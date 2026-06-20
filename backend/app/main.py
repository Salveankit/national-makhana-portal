from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import csv
import io
import json

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles

from backend.app.core.config import settings
from backend.app.core.security import issue_token, verify_password
from backend.app.chatbot import answer_chat, chat_analytics_snapshot
from backend.app.data import (
    add_audit,
    create_application,
    get_aap,
    get_application,
    get_beneficiary_profile as load_beneficiary_profile,
    get_budget,
    get_inspection,
    get_open_clarification,
    get_user_by_id,
    get_user_by_email,
    list_chat_logs,
    list_integration_events,
    list_aap as load_aap,
    list_audit_logs,
    list_beneficiary_applications as load_beneficiary_applications,
    list_budgets as load_budgets,
    list_clarifications as load_clarifications,
    list_field_data as load_field_data,
    list_inspections as load_inspections,
    list_locations,
    list_notifications,
    list_officer_applications,
    next_aap_id,
    next_application_id,
    next_budget_id,
    next_chat_id,
    next_clarification_id,
    next_field_data_id,
    next_integration_event_id,
    next_inspection_id,
    next_notification_id,
    save_aap,
    save_application,
    save_beneficiary_profile as persist_beneficiary_profile,
    save_budget,
    save_clarification,
    save_field_data,
    save_integration_event,
    save_inspection,
    save_chat_log,
    save_notification,
    storage_health,
)
from backend.app.deps import get_current_user, get_optional_user, require_permission
from backend.app.models import (
    AnnualActionPlan,
    ApplicationRecord,
    BeneficiaryProfile,
    BudgetRecord,
    ChatInteractionRecord,
    ClarificationRecord,
    DocumentMeta,
    FieldDataRecord,
    GeoTag,
    IntegrationEventRecord,
    InspectionRecord,
    NotificationRecord,
    StatusEntry,
)
from backend.app.schemas import (
    AAPRequest,
    AAPReviewRequest,
    AadhaarVerificationRequest,
    ApplicationRequest,
    BatchDecisionRequest,
    BeneficiaryProfileRequest,
    BudgetRequest,
    BudgetUtilizationRequest,
    ChatAction,
    ChatMessageRequest,
    ChatMessageResponse,
    ChatSource,
    ClarificationRequest,
    ClarificationResponseRequest,
    DecisionRequest,
    FieldDataRequest,
    InspectionAssignRequest,
    InspectionCompleteRequest,
    LoginRequest,
    LoginResponse,
    MockAadhaarKycRequest,
    MockDBTRequest,
    MockNotificationRequest,
    RecommendationRequest,
)

app = FastAPI(title=settings.app_name, version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/assets", StaticFiles(directory=frontend_dir / "assets"), name="assets")

ALLOWED_DOCUMENT_TYPES = {"identity_proof", "bank_proof", "land_record", "inspection_photo"}
ALLOWED_FILE_SUFFIXES = {".pdf", ".jpg", ".jpeg", ".png"}


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com data:; "
        "script-src 'self' 'unsafe-inline'"
    )
    return response


def _request_ip(request: Request) -> str:
    return request.client.host if request.client else "unknown"


def _scoped_applications(user):
    return list_officer_applications(user.role, user.email)


def _validate_document_request(file_name: str, document_type: str) -> None:
    suffix = Path(file_name).suffix.lower()
    if document_type not in ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported document type: {document_type}")
    if suffix not in ALLOWED_FILE_SUFFIXES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix or 'unknown'}")
    if ".." in file_name or "/" in file_name or "\\" in file_name:
        raise HTTPException(status_code=400, detail="Unsafe file name")


def _mask_aadhaar(aadhaar_number: str) -> str:
    digits = "".join(ch for ch in aadhaar_number if ch.isdigit())
    if len(digits) != 12:
        raise HTTPException(status_code=400, detail="Aadhaar number must contain 12 digits")
    return f"XXXX-XXXX-{digits[-4:]}"


def _vault_reference(aadhaar_number: str, user_id: str) -> str:
    digits = "".join(ch for ch in aadhaar_number if ch.isdigit())
    return f"vault-{user_id}-{digits[-4:]}"


def _validate_notification_recipient(channel: str, recipient: str) -> str:
    normalized_channel = channel.strip().lower()
    if normalized_channel in {"sms", "whatsapp"}:
        digits = "".join(ch for ch in recipient if ch.isdigit())
        if len(digits) != 10:
            raise HTTPException(status_code=400, detail=f"{normalized_channel.upper()} recipient must be a 10 digit mobile number")
        return digits
    if normalized_channel == "email":
        clean_email = recipient.strip()
        if "@" not in clean_email or "." not in clean_email.split("@")[-1]:
            raise HTTPException(status_code=400, detail="Email recipient must be a valid email address")
        return clean_email
    raise HTTPException(status_code=400, detail="Channel must be sms, email, or whatsapp")


def emit_notification(event_key: str, module: str, recipient: str, subject: str, message: str, channels: list[str] | None = None):
    now = datetime.now(UTC).isoformat()
    requested_channels = channels or ["in_app", "email", "sms"]
    provider_results = {"in_app": "logged"}
    delivered_channels = ["in_app"]
    if "email" in requested_channels:
        provider_results["email"] = "delivered" if settings.email_gateway_enabled else "configured"
        delivered_channels.append("email")
    if "sms" in requested_channels:
        provider_results["sms"] = "delivered" if settings.sms_gateway_enabled else "awaiting_credentials"
        delivered_channels.append("sms")
    if "whatsapp" in requested_channels:
        provider_results["whatsapp"] = "delivered" if settings.whatsapp_gateway_enabled else "awaiting_credentials"
        delivered_channels.append("whatsapp")
    record = NotificationRecord(
        notification_id=next_notification_id(),
        event_key=event_key,
        module=module,
        recipient=recipient,
        channels=delivered_channels,
        subject=subject,
        message=message,
        status="delivered" if all(value == "delivered" for key, value in provider_results.items() if key != "in_app") else "logged",
        created_at=now,
        delivered_at=now,
        provider_results=provider_results,
    )
    save_notification(record)
    return record


def _mock_provider_status(provider_name: str) -> str:
    provider_map = {
        "mock-sms-gateway": "ready_for_live_swap",
        "mock-email-gateway": "ready_for_live_swap",
        "mock-whatsapp-gateway": "requires_business_credentials",
        "mock-aadhaar-vault": "mock_mode",
        "mock-dbt-switch": "banking_integration_pending",
    }
    return provider_map.get(provider_name, "mock_mode")


def record_integration_event(
    integration_type: str,
    provider_name: str,
    action: str,
    request_payload: dict,
    response_payload: dict,
    status: str | None = None,
):
    record = IntegrationEventRecord(
        event_id=next_integration_event_id(),
        integration_type=integration_type,
        provider_name=provider_name,
        action=action,
        status=status or _mock_provider_status(provider_name),
        request_payload=request_payload,
        response_payload=response_payload,
        created_at=datetime.now(UTC).isoformat(),
    )
    save_integration_event(record)
    return record


@app.get("/health")
def health():
    services = storage_health()
    overall = "ok" if services["sqlite"] == "up" and services["documents"] == "up" else "degraded"
    return {
        "status": overall,
        "app": settings.app_name,
        "environment": settings.app_env,
        "services": {"api": "up", **services},
    }


@app.post("/api/v1/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, request: Request):
    user = get_user_by_email(payload.email)
    ip = _request_ip(request)
    if not user or not verify_password(payload.password, user.password_hash):
        add_audit(payload.email, "anonymous", "login_failed", "auth", "Invalid credentials", ip)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    add_audit(user.email, user.role, "login", "auth", "User signed in", ip)
    return LoginResponse(access_token=issue_token(user.email, user.role), role=user.role, name=user.name)


@app.get("/api/v1/auth/me")
def me(user=Depends(get_current_user)):
    return {"email": user.email, "name": user.name, "role": user.role, "state_code": user.state_code}


@app.get("/api/v1/locations/states")
def states(user=Depends(require_permission("locations:read"))):
    return list_locations("state")


@app.get("/api/v1/locations/districts")
def districts(state_code: str, user=Depends(require_permission("locations:read"))):
    return list_locations("district", state_code)


@app.get("/api/v1/locations/blocks")
def blocks(district_code: str, user=Depends(require_permission("locations:read"))):
    return list_locations("block", district_code)


@app.get("/api/v1/locations/villages")
def villages(block_code: str, user=Depends(require_permission("locations:read"))):
    return list_locations("village", block_code)


@app.get("/api/v1/audit/logs")
def audit_logs(user=Depends(require_permission("audit:read"))):
    return list_audit_logs(100)


@app.get("/api/v1/notifications")
def notifications(limit: int = 100, user=Depends(get_current_user)):
    if user.role == "beneficiary":
        return list_notifications(limit, user.email)
    if user.role not in {"state_officer", "inspector", "nmb_admin"}:
        raise HTTPException(status_code=403, detail="Not allowed")
    return list_notifications(limit)


@app.get("/api/v1/system/overview")
def system_overview(user=Depends(get_current_user)):
    if user.role not in {"nmb_admin", "state_officer"}:
        raise HTTPException(status_code=403, detail="Admin or state operations only")
    audits = list_audit_logs(20)
    notifications_log = list_notifications(20)
    services = storage_health()
    failed_security = [entry for entry in audits if entry.action in {"login_failed", "deny"}][:5]
    recent_failures = [
        {
            "timestamp": entry.timestamp,
            "module": entry.module,
            "action": entry.action,
            "detail": entry.detail,
        }
        for entry in failed_security
    ]
    return {
        "services": services,
        "integrations": {
            "sms_gateway": "connected" if settings.sms_gateway_enabled else "awaiting_credentials",
            "email_gateway": "connected" if settings.email_gateway_enabled else "awaiting_credentials",
            "whatsapp_gateway": "connected" if settings.whatsapp_gateway_enabled else "awaiting_credentials",
            "aadhaar_vault": "connected" if settings.aadhaar_vault_enabled else "mock_mode",
        },
        "queue_health": {
            "open_clarifications": len([item for item in load_clarifications() if item.status == "Open"]),
            "pending_inspections": len([item for item in load_inspections("nmb_admin", user.email) if item.status != "Completed"]),
            "pending_applications": len([item for item in list_officer_applications("nmb_admin", user.email) if item.current_status not in {"Approved", "Rejected"}]),
        },
        "notification_summary": {
            "logged": len(notifications_log),
            "latest": [item.model_dump() for item in notifications_log[:8]],
        },
        "recent_failures": recent_failures,
    }


@app.get("/api/v1/integrations/mock/logs")
def mock_integration_logs(limit: int = 30, integration_type: str | None = None, user=Depends(get_current_user)):
    if user.role not in {"nmb_admin", "state_officer"}:
        raise HTTPException(status_code=403, detail="Admin or state operations only")
    return list_integration_events(limit, integration_type)


@app.get("/api/v1/integrations/mock/catalog")
def mock_integration_catalog(user=Depends(get_current_user)):
    if user.role not in {"nmb_admin", "state_officer"}:
        raise HTTPException(status_code=403, detail="Admin or state operations only")
    return {
        "items": [
            {"integration_type": "notification", "provider_name": "mock-sms-gateway", "status": _mock_provider_status("mock-sms-gateway")},
            {"integration_type": "notification", "provider_name": "mock-email-gateway", "status": _mock_provider_status("mock-email-gateway")},
            {"integration_type": "notification", "provider_name": "mock-whatsapp-gateway", "status": _mock_provider_status("mock-whatsapp-gateway")},
            {"integration_type": "identity", "provider_name": "mock-aadhaar-vault", "status": _mock_provider_status("mock-aadhaar-vault")},
            {"integration_type": "payments", "provider_name": "mock-dbt-switch", "status": _mock_provider_status("mock-dbt-switch")},
        ]
    }


@app.post("/api/v1/integrations/mock/notify")
def mock_notify(payload: MockNotificationRequest, request: Request, user=Depends(get_current_user)):
    if user.role not in {"nmb_admin", "state_officer"}:
        raise HTTPException(status_code=403, detail="Admin or state operations only")
    channel = payload.channel.strip().lower()
    recipient = _validate_notification_recipient(channel, payload.recipient)
    provider_map = {
        "sms": "mock-sms-gateway",
        "email": "mock-email-gateway",
        "whatsapp": "mock-whatsapp-gateway",
    }
    provider_name = provider_map.get(channel)
    if not provider_name:
        raise HTTPException(status_code=400, detail="Channel must be sms, email, or whatsapp")
    request_payload = payload.model_dump()
    request_payload["channel"] = channel
    request_payload["recipient"] = recipient
    event = record_integration_event(
        "notification",
        provider_name,
        "send_template_message",
        request_payload=request_payload,
        response_payload={
            "provider_reference": f"{provider_name}-{datetime.now(UTC).strftime('%H%M%S')}",
            "delivery_state": _mock_provider_status(provider_name),
            "template_preview": payload.template_key,
        },
    )
    add_audit(user.email, user.role, "mock_send", "integration_notification", f"Triggered {channel} notification", _request_ip(request))
    return event


@app.post("/api/v1/integrations/mock/aadhaar-kyc")
def mock_aadhaar_kyc(payload: MockAadhaarKycRequest, request: Request, user=Depends(get_current_user)):
    if user.role not in {"nmb_admin", "state_officer"}:
        raise HTTPException(status_code=403, detail="Admin or state operations only")
    if not payload.consent:
        raise HTTPException(status_code=400, detail="Consent is required")
    masked = _mask_aadhaar(payload.aadhaar_number)
    event = record_integration_event(
        "identity",
        "mock-aadhaar-vault",
        "kyc_verify",
        request_payload={"beneficiary_name": payload.beneficiary_name, "aadhaar_masked": masked, "consent": payload.consent},
        response_payload={
            "verification_status": "verified",
            "vault_reference": _vault_reference(payload.aadhaar_number, "demo"),
            "name_match_score": "0.98",
        },
    )
    add_audit(user.email, user.role, "mock_verify", "integration_identity", f"Triggered mock Aadhaar KYC for {payload.beneficiary_name}", _request_ip(request))
    return event


@app.post("/api/v1/integrations/mock/dbt/disburse")
def mock_dbt_disburse(payload: MockDBTRequest, request: Request, user=Depends(get_current_user)):
    if user.role not in {"nmb_admin", "state_officer"}:
        raise HTTPException(status_code=403, detail="Admin or state operations only")
    event = record_integration_event(
        "payments",
        "mock-dbt-switch",
        "disburse",
        request_payload=payload.model_dump(),
        response_payload={
            "disbursement_reference": f"DBT-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}",
            "beneficiary_account_masked": f"XXXXXX{payload.bank_account_last4}",
            "transaction_status": "queued_for_department_approval",
        },
    )
    add_audit(user.email, user.role, "mock_disburse", "integration_payments", f"Triggered mock DBT for {payload.application_id}", _request_ip(request))
    return event


@app.get("/api/v1/beneficiary/profile")
def get_beneficiary_profile(request: Request, user=Depends(get_current_user)):
    if user.role != "beneficiary":
        raise HTTPException(status_code=403, detail="Beneficiary only")
    profile = load_beneficiary_profile(user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    add_audit(user.email, user.role, "read", "beneficiary_profile", "Viewed profile", _request_ip(request))
    return profile


@app.put("/api/v1/beneficiary/profile")
def save_beneficiary_profile(payload: BeneficiaryProfileRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "beneficiary":
        raise HTTPException(status_code=403, detail="Beneficiary only")
    profile = BeneficiaryProfile(
        user_id=user.id,
        name=payload.name,
        aadhaar_masked="XXXX-XXXX-1234",
        mobile=payload.mobile,
        email=user.email,
        state_code=payload.state_code,
        district_code=payload.district_code,
        block_code=payload.block_code,
        village_code=payload.village_code,
        cultivation_type=payload.cultivation_type,
        total_land_acres=payload.total_land_acres,
        makhana_area_acres=payload.makhana_area_acres,
    )
    persist_beneficiary_profile(profile)
    add_audit(user.email, user.role, "update", "beneficiary_profile", "Saved beneficiary profile", _request_ip(request))
    emit_notification("beneficiary.profile.saved", "beneficiary_profile", user.email, "Profile saved", "Your beneficiary profile has been saved successfully.")
    return profile


@app.post("/api/v1/beneficiary/profile/verify-aadhaar")
def verify_beneficiary_identity(payload: AadhaarVerificationRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "beneficiary":
        raise HTTPException(status_code=403, detail="Beneficiary only")
    if not payload.consent:
        raise HTTPException(status_code=400, detail="Consent is required for identity verification")
    profile = load_beneficiary_profile(user.id)
    if not profile:
        raise HTTPException(status_code=400, detail="Profile required before verification")
    profile.aadhaar_masked = _mask_aadhaar(payload.aadhaar_number)
    profile.aadhaar_vault_ref = _vault_reference(payload.aadhaar_number, user.id)
    profile.identity_verified = True
    persist_beneficiary_profile(profile)
    add_audit(user.email, user.role, "verify", "beneficiary_identity", "Beneficiary identity tokenized for vault flow", _request_ip(request))
    emit_notification(
        "beneficiary.identity.verified",
        "beneficiary_identity",
        user.email,
        "Identity verified",
        "Your Aadhaar identity has been tokenized and verified for scheme processing.",
        ["in_app", "email"],
    )
    return {
        "aadhaar_masked": profile.aadhaar_masked,
        "aadhaar_vault_ref": profile.aadhaar_vault_ref,
        "identity_verified": profile.identity_verified,
        "vault_mode": "live" if settings.aadhaar_vault_enabled else "mock",
    }


@app.get("/api/v1/beneficiary/applications")
def list_beneficiary_applications(user=Depends(get_current_user)):
    if user.role != "beneficiary":
        raise HTTPException(status_code=403, detail="Beneficiary only")
    return load_beneficiary_applications(user.id)


@app.post("/api/v1/beneficiary/applications")
def create_beneficiary_application(payload: ApplicationRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "beneficiary":
        raise HTTPException(status_code=403, detail="Beneficiary only")
    profile = load_beneficiary_profile(user.id)
    if not profile:
        raise HTTPException(status_code=400, detail="Profile required before application submission")
    for doc in payload.documents:
        _validate_document_request(doc.file_name, doc.document_type)
    now = datetime.now(UTC).isoformat()
    application_id = next_application_id(profile.state_code)
    record = ApplicationRecord(
        application_id=application_id,
        beneficiary_user_id=user.id,
        scheme_component=payload.scheme_component,
        pond_area_acres=payload.pond_area_acres,
        requested_amount=payload.requested_amount,
        current_status="Submitted",
        assigned_state_officer="bihar.officer@example.com",
        geo_tag=GeoTag(**payload.geo_tag.model_dump(), captured_at=now) if payload.geo_tag else None,
        documents=[
            DocumentMeta(
                document_id=f"{application_id}-DOC-{index + 1}",
                file_name=doc.file_name,
                document_type=doc.document_type,
                uploaded_at=now,
            )
            for index, doc in enumerate(payload.documents)
        ],
        status_history=[
            StatusEntry(status="Draft", remarks="Application prepared in portal", changed_at=now),
            StatusEntry(status="Submitted", remarks="Application submitted successfully", changed_at=now),
        ],
    )
    create_application(record)
    add_audit(user.email, user.role, "create", "application", f"Created application {application_id}", _request_ip(request))
    emit_notification("application.submitted", "application", user.email, "Application submitted", f"Application {application_id} has been submitted.")
    emit_notification("application.submitted", "application", record.assigned_state_officer or "bihar.officer@example.com", "New application submitted", f"Application {application_id} requires state review.")
    return record


@app.get("/api/v1/beneficiary/applications/{application_id}")
def get_beneficiary_application(application_id: str, user=Depends(get_current_user)):
    if user.role != "beneficiary":
        raise HTTPException(status_code=403, detail="Beneficiary only")
    record = get_application(application_id)
    if not record or record.beneficiary_user_id != user.id:
        raise HTTPException(status_code=404, detail="Application not found")
    return record


@app.post("/api/v1/beneficiary/applications/{application_id}/clarifications/respond")
def respond_to_clarification(application_id: str, payload: ClarificationResponseRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "beneficiary":
        raise HTTPException(status_code=403, detail="Beneficiary only")
    record = get_application(application_id)
    if not record or record.beneficiary_user_id != user.id:
        raise HTTPException(status_code=404, detail="Application not found")
    clarification = get_open_clarification(application_id)
    if not clarification:
        raise HTTPException(status_code=404, detail="Open clarification not found")
    now = datetime.now(UTC).isoformat()
    clarification.response_text = payload.response_text
    clarification.responded_by = user.email
    clarification.responded_at = now
    clarification.status = "Responded"
    record.current_status = "Resubmitted"
    record.status_history.insert(0, StatusEntry(status="Resubmitted", remarks="Beneficiary responded to clarification", changed_at=now))
    save_clarification(clarification)
    save_application(record)
    add_audit(user.email, user.role, "respond", "clarification", f"Responded to {clarification.clarification_id}", _request_ip(request))
    emit_notification("clarification.responded", "clarification", record.assigned_state_officer or "bihar.officer@example.com", "Clarification responded", f"Beneficiary responded for {application_id}.")
    return clarification


@app.get("/api/v1/officer/applications")
def officer_queue(user=Depends(get_current_user)):
    if user.role not in {"state_officer", "inspector", "nmb_admin"}:
        raise HTTPException(status_code=403, detail="Officer only")
    return _scoped_applications(user)


@app.post("/api/v1/officer/applications/{application_id}/clarifications")
def raise_clarification(application_id: str, payload: ClarificationRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "state_officer":
        raise HTTPException(status_code=403, detail="State officer only")
    record = get_application(application_id)
    if not record:
        raise HTTPException(status_code=404, detail="Application not found")
    now = datetime.now(UTC).isoformat()
    clarification_id = next_clarification_id()
    clarification = ClarificationRecord(
        clarification_id=clarification_id,
        application_id=application_id,
        query_text=payload.query_text,
        raised_by=user.email,
        status="Open",
        raised_at=now,
    )
    record.current_status = "Clarification Raised"
    record.status_history.insert(0, StatusEntry(status="Clarification Raised", remarks=payload.query_text, changed_at=now))
    save_clarification(clarification)
    save_application(record)
    add_audit(user.email, user.role, "create", "clarification", f"Raised {clarification_id} for {application_id}", _request_ip(request))
    beneficiary_user = get_user_by_id(record.beneficiary_user_id)
    recipient = beneficiary_user.email if beneficiary_user else "farmer@example.com"
    emit_notification("clarification.raised", "clarification", recipient, "Clarification requested", f"Clarification has been raised on application {application_id}.")
    return clarification


@app.post("/api/v1/officer/applications/{application_id}/inspection/assign")
def assign_inspection(application_id: str, payload: InspectionAssignRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "state_officer":
        raise HTTPException(status_code=403, detail="State officer only")
    record = get_application(application_id)
    if not record:
        raise HTTPException(status_code=404, detail="Application not found")
    now = datetime.now(UTC).isoformat()
    inspection_id = next_inspection_id()
    inspection = InspectionRecord(
        inspection_id=inspection_id,
        application_id=application_id,
        inspector_email=payload.inspector_email,
        assigned_by=user.email,
        status="Assigned",
        assigned_at=now,
    )
    record.assigned_inspector = payload.inspector_email
    record.current_status = "Inspection Assigned"
    record.status_history.insert(0, StatusEntry(status="Inspection Assigned", remarks=f"Assigned to {payload.inspector_email}", changed_at=now))
    save_inspection(inspection)
    save_application(record)
    add_audit(user.email, user.role, "assign", "inspection", f"Assigned {inspection_id} for {application_id}", _request_ip(request))
    emit_notification("inspection.assigned", "inspection", payload.inspector_email, "Inspection assigned", f"You have been assigned inspection {inspection_id} for application {application_id}.")
    return inspection


@app.post("/api/v1/officer/inspections/{inspection_id}/complete")
def complete_inspection(inspection_id: str, payload: InspectionCompleteRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "inspector":
        raise HTTPException(status_code=403, detail="Inspector only")
    inspection = get_inspection(inspection_id)
    if not inspection or inspection.inspector_email != user.email:
        raise HTTPException(status_code=404, detail="Inspection not found")
    record = get_application(inspection.application_id)
    now = datetime.now(UTC).isoformat()
    inspection.status = "Completed"
    inspection.remarks = payload.remarks
    inspection.geo_tag = GeoTag(latitude=payload.latitude, longitude=payload.longitude, accuracy=payload.accuracy, captured_at=now)
    inspection.photos = [
        DocumentMeta(
            document_id=f"{inspection_id}-PHOTO-1",
            file_name=payload.photo_name,
            document_type="inspection_photo",
            uploaded_at=now,
        )
    ]
    inspection.completed_at = now
    save_inspection(inspection)
    if record:
        record.current_status = "Inspection Completed"
        record.status_history.insert(0, StatusEntry(status="Inspection Completed", remarks=payload.remarks, changed_at=now))
        save_application(record)
    add_audit(user.email, user.role, "complete", "inspection", f"Completed {inspection_id}", _request_ip(request))
    emit_notification("inspection.completed", "inspection", record.assigned_state_officer if record else "bihar.officer@example.com", "Inspection completed", f"Inspection {inspection_id} has been completed for application {inspection.application_id}.")
    return inspection


@app.post("/api/v1/officer/applications/{application_id}/recommend")
def recommend_application(application_id: str, payload: RecommendationRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "state_officer":
        raise HTTPException(status_code=403, detail="State officer only")
    record = get_application(application_id)
    if not record:
        raise HTTPException(status_code=404, detail="Application not found")
    now = datetime.now(UTC).isoformat()
    record.current_status = "Recommended by State"
    record.recommendation_note = payload.remarks
    record.status_history.insert(0, StatusEntry(status="Recommended by State", remarks=payload.remarks, changed_at=now))
    save_application(record)
    add_audit(user.email, user.role, "recommend", "application", f"Recommended {application_id}", _request_ip(request))
    emit_notification("application.recommended", "application", "nmb.admin@example.com", "Application recommended", f"Application {application_id} is recommended by state for board review.")
    return record


@app.post("/api/v1/nmb/applications/{application_id}/decision")
def board_decision(application_id: str, payload: DecisionRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "nmb_admin":
        raise HTTPException(status_code=403, detail="NMB admin only")
    record = get_application(application_id)
    if not record:
        raise HTTPException(status_code=404, detail="Application not found")
    decision = payload.decision.strip().title()
    if decision not in {"Approved", "Rejected", "Returned"}:
        raise HTTPException(status_code=400, detail="Decision must be Approved, Rejected, or Returned")
    now = datetime.now(UTC).isoformat()
    record.current_status = decision
    record.decision_note = payload.remarks
    record.status_history.insert(0, StatusEntry(status=decision, remarks=payload.remarks, changed_at=now))
    save_application(record)
    add_audit(user.email, user.role, "decide", "application", f"{decision} {application_id}", _request_ip(request))
    beneficiary_user = get_user_by_id(record.beneficiary_user_id)
    beneficiary_email = beneficiary_user.email if beneficiary_user else "farmer@example.com"
    emit_notification(f"application.{decision.lower()}", "application", beneficiary_email, f"Application {decision}", f"Your application {application_id} has been {decision.lower()}.")
    return record


@app.post("/api/v1/nmb/applications/batch-decision")
def batch_board_decision(payload: BatchDecisionRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "nmb_admin":
        raise HTTPException(status_code=403, detail="NMB admin only")
    if not payload.application_ids:
        raise HTTPException(status_code=400, detail="At least one application id is required")
    results = []
    for application_id in payload.application_ids:
        record = get_application(application_id)
        if not record:
            results.append({"application_id": application_id, "status": "not_found"})
            continue
        decision_payload = DecisionRequest(decision=payload.decision, remarks=payload.remarks)
        updated = board_decision(application_id, decision_payload, request, user)
        results.append({"application_id": application_id, "status": updated.current_status})
    add_audit(user.email, user.role, "batch_decide", "application", f"Processed batch decision for {len(payload.application_ids)} applications", _request_ip(request))
    return {"processed": results, "decision": payload.decision.strip().title()}


@app.get("/api/v1/officer/clarifications")
def list_clarifications(user=Depends(get_current_user)):
    if user.role not in {"state_officer", "beneficiary", "nmb_admin"}:
        raise HTTPException(status_code=403, detail="Not allowed")
    if user.role == "beneficiary":
        allowed_ids = {item.application_id for item in load_beneficiary_applications(user.id)}
        return load_clarifications(allowed_ids)
    return load_clarifications()


@app.get("/api/v1/officer/inspections")
def list_inspections(user=Depends(get_current_user)):
    if user.role not in {"state_officer", "inspector", "nmb_admin"}:
        raise HTTPException(status_code=403, detail="Not allowed")
    return load_inspections(user.role, user.email)


@app.get("/api/v1/aap")
def list_aap(financial_year: str | None = None, current_status: str | None = None, user=Depends(get_current_user)):
    if user.role not in {"state_officer", "nmb_admin"}:
        raise HTTPException(status_code=403, detail="Not allowed")
    return load_aap(user.role, user.email, user.state_code, financial_year, current_status)


@app.post("/api/v1/aap")
def create_aap(payload: AAPRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "state_officer":
        raise HTTPException(status_code=403, detail="State officer only")
    now = datetime.now(UTC).isoformat()
    state_code = user.state_code or "BR"
    aap_id = next_aap_id(state_code, payload.financial_year)
    record = AnnualActionPlan(
        aap_id=aap_id,
        state_code=state_code,
        financial_year=payload.financial_year,
        cultivation_target_hectares=payload.cultivation_target_hectares,
        farmer_target=payload.farmer_target,
        infrastructure_target=payload.infrastructure_target,
        budget_requested=payload.budget_requested,
        current_status="Submitted",
        submitted_by=user.email,
        submitted_at=now,
        remarks=payload.remarks,
        status_history=[
            StatusEntry(status="Draft", remarks="Plan prepared in state workspace", changed_at=now),
            StatusEntry(status="Submitted", remarks=payload.remarks, changed_at=now),
        ],
    )
    save_aap(record)
    add_audit(user.email, user.role, "create", "aap", f"Created {aap_id}", _request_ip(request))
    emit_notification("aap.submitted", "aap", "nmb.admin@example.com", "AAP submitted", f"AAP {aap_id} has been submitted for review.")
    return record


@app.post("/api/v1/aap/{aap_id}/review")
def review_aap(aap_id: str, payload: AAPReviewRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "nmb_admin":
        raise HTTPException(status_code=403, detail="NMB admin only")
    record = get_aap(aap_id)
    if not record:
        raise HTTPException(status_code=404, detail="AAP not found")
    decision_map = {
        "query raised": "Query Raised",
        "returned": "Returned",
        "approved": "Approved",
    }
    decision_key = payload.decision.strip().lower()
    if decision_key not in decision_map:
        raise HTTPException(status_code=400, detail="Decision must be Query Raised, Returned, or Approved")
    new_status = decision_map[decision_key]
    now = datetime.now(UTC).isoformat()
    record.current_status = new_status
    record.remarks = payload.remarks
    record.status_history.insert(0, StatusEntry(status=new_status, remarks=payload.remarks, changed_at=now))
    save_aap(record)
    add_audit(user.email, user.role, "review", "aap", f"{new_status} {aap_id}", _request_ip(request))
    emit_notification(f"aap.{new_status.lower().replace(' ', '_')}", "aap", record.submitted_by, f"AAP {new_status}", f"AAP {aap_id} status updated to {new_status}.")
    return record


@app.get("/api/v1/field-data")
def list_field_data(
    district_code: str | None = None,
    financial_year: str | None = None,
    quarter: str | None = None,
    user=Depends(get_current_user),
):
    if user.role not in {"state_officer", "nmb_admin"}:
        raise HTTPException(status_code=403, detail="Not allowed")
    return load_field_data(user.role, user.state_code, district_code, financial_year, quarter)


@app.post("/api/v1/field-data")
def create_field_data(payload: FieldDataRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "state_officer":
        raise HTTPException(status_code=403, detail="State officer only")
    now = datetime.now(UTC).isoformat()
    record = FieldDataRecord(
        field_data_id=next_field_data_id(),
        state_code=user.state_code or "BR",
        district_code=payload.district_code,
        financial_year=payload.financial_year,
        quarter=payload.quarter,
        area_hectares=payload.area_hectares,
        production_mt=payload.production_mt,
        farmer_count=payload.farmer_count,
        processing_units=payload.processing_units,
        entered_by=user.email,
        entered_at=now,
    )
    save_field_data(record)
    add_audit(user.email, user.role, "create", "field_data", f"Created {record.field_data_id}", _request_ip(request))
    return record


@app.get("/api/v1/budgets")
def list_budgets(financial_year: str | None = None, component_name: str | None = None, user=Depends(get_current_user)):
    if user.role not in {"state_officer", "nmb_admin"}:
        raise HTTPException(status_code=403, detail="Not allowed")
    return load_budgets(user.role, user.state_code, financial_year, component_name)


@app.post("/api/v1/budgets")
def create_budget(payload: BudgetRequest, request: Request, user=Depends(get_current_user)):
    if user.role != "nmb_admin":
        raise HTTPException(status_code=403, detail="NMB admin only")
    now = datetime.now(UTC).isoformat()
    record = BudgetRecord(
        budget_id=next_budget_id(payload.state_code),
        state_code=payload.state_code,
        component_name=payload.component_name,
        financial_year=payload.financial_year,
        allocated_amount=payload.allocated_amount,
        released_amount=payload.released_amount,
        utilized_amount=payload.utilized_amount,
        updated_by=user.email,
        updated_at=now,
        remarks="Initial allocation entry by NMB admin",
    )
    save_budget(record)
    add_audit(user.email, user.role, "create", "budget", f"Created {record.budget_id}", _request_ip(request))
    emit_notification("budget.allocated", "budget", "bihar.officer@example.com", "Budget allocated", f"Budget {record.budget_id} has been allocated for {record.component_name}.")
    return record


@app.post("/api/v1/budgets/{budget_id}/utilization")
def update_budget_utilization(budget_id: str, payload: BudgetUtilizationRequest, request: Request, user=Depends(get_current_user)):
    if user.role not in {"state_officer", "nmb_admin"}:
        raise HTTPException(status_code=403, detail="Not allowed")
    record = get_budget(budget_id)
    if not record:
        raise HTTPException(status_code=404, detail="Budget not found")
    if user.role == "state_officer" and record.state_code != user.state_code:
        raise HTTPException(status_code=403, detail="State-scoped budget only")
    record.released_amount = payload.released_amount
    record.utilized_amount = payload.utilized_amount
    record.remarks = payload.remarks
    record.updated_by = user.email
    record.updated_at = datetime.now(UTC).isoformat()
    save_budget(record)
    add_audit(user.email, user.role, "update", "budget", f"Updated utilization for {budget_id}", _request_ip(request))
    emit_notification("budget.utilization.updated", "budget", "nmb.admin@example.com", "Budget utilization updated", f"Budget {budget_id} utilization has been updated by {user.email}.")
    return record


@app.get("/api/v1/dashboard/summary")
def dashboard_summary(
    financial_year: str | None = None,
    state_code: str | None = None,
    district_code: str | None = None,
    quarter: str | None = None,
    user=Depends(get_current_user),
):
    if user.role not in {"state_officer", "inspector", "nmb_admin"}:
        raise HTTPException(status_code=403, detail="Officer only")
    scoped_apps = _scoped_applications(user) if user.role != "nmb_admin" else list_officer_applications("nmb_admin", user.email)
    scoped_fields = load_field_data(
        "nmb_admin" if user.role == "nmb_admin" else "state_officer",
        state_code if user.role == "nmb_admin" and state_code else user.state_code,
        district_code,
        financial_year,
        quarter,
    )
    scoped_budgets = load_budgets(
        "nmb_admin" if user.role == "nmb_admin" else "state_officer",
        state_code if user.role == "nmb_admin" and state_code else user.state_code,
        financial_year,
        None,
    )
    scoped_aaps = load_aap(
        "nmb_admin" if user.role == "nmb_admin" else "state_officer",
        user.email,
        state_code if user.role == "nmb_admin" and state_code else user.state_code,
        financial_year,
        None,
    )

    total_area = round(sum(item.area_hectares for item in scoped_fields), 2)
    total_production = round(sum(item.production_mt for item in scoped_fields), 2)
    total_farmers = sum(item.farmer_count for item in scoped_fields)
    allocated = sum(item.allocated_amount for item in scoped_budgets)
    utilized = sum(item.utilized_amount for item in scoped_budgets)

    by_status: dict[str, int] = {}
    for item in scoped_apps:
        by_status[item.current_status] = by_status.get(item.current_status, 0) + 1

    state_cards: dict[str, dict[str, float | int | str]] = {}
    for item in scoped_fields:
        card = state_cards.setdefault(
            item.state_code,
            {"state_code": item.state_code, "area_hectares": 0.0, "production_mt": 0.0, "farmer_count": 0},
        )
        card["area_hectares"] += item.area_hectares
        card["production_mt"] += item.production_mt
        card["farmer_count"] += item.farmer_count

    trend_points: dict[str, dict[str, float | int | str]] = {}
    for item in scoped_fields:
        point = trend_points.setdefault(
            item.quarter,
            {"quarter": item.quarter, "area_hectares": 0.0, "production_mt": 0.0, "farmer_count": 0},
        )
        point["area_hectares"] += item.area_hectares
        point["production_mt"] += item.production_mt
        point["farmer_count"] += item.farmer_count

    return {
        "filters": {
            "financial_year": financial_year,
            "state_code": state_code if user.role == "nmb_admin" else user.state_code,
            "district_code": district_code,
            "quarter": quarter,
        },
        "kpis": {
            "applications": len(scoped_apps),
            "approved": by_status.get("Approved", 0),
            "pending": len([item for item in scoped_apps if item.current_status not in {"Approved", "Rejected"}]),
            "area_hectares": total_area,
            "production_mt": total_production,
            "farmers": total_farmers,
            "allocated_budget": allocated,
            "utilized_budget": utilized,
            "aap_submissions": len(scoped_aaps),
        },
        "status_breakdown": by_status,
        "district_cards": [
            {
                "district_code": item.district_code,
                "state_code": item.state_code,
                "financial_year": item.financial_year,
                "quarter": item.quarter,
                "area_hectares": item.area_hectares,
                "production_mt": item.production_mt,
                "farmer_count": item.farmer_count,
            }
            for item in scoped_fields
        ],
        "budget_cards": [
            {
                "component_name": item.component_name,
                "allocated_amount": item.allocated_amount,
                "released_amount": item.released_amount,
                "utilized_amount": item.utilized_amount,
            }
            for item in scoped_budgets
        ],
        "state_cards": list(state_cards.values()),
        "trend_points": list(trend_points.values()),
        "aap_cards": [
            {
                "aap_id": item.aap_id,
                "state_code": item.state_code,
                "financial_year": item.financial_year,
                "budget_requested": item.budget_requested,
                "current_status": item.current_status,
                "status_history": [entry.model_dump() for entry in item.status_history],
            }
            for item in scoped_aaps
        ],
    }


@app.get("/api/v1/reports/overview")
def report_overview(
    format: str = "json",
    financial_year: str | None = None,
    state_code: str | None = None,
    district_code: str | None = None,
    quarter: str | None = None,
    user=Depends(get_current_user),
):
    summary = dashboard_summary(financial_year, state_code, district_code, quarter, user)
    if format.lower() == "csv":
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["metric", "value"])
        for key, value in summary["kpis"].items():
            writer.writerow([key, value])
        writer.writerow([])
        writer.writerow(["district_code", "state_code", "financial_year", "quarter", "area_hectares", "production_mt", "farmer_count"])
        for row in summary["district_cards"]:
            writer.writerow([
                row["district_code"],
                row["state_code"],
                row["financial_year"],
                row["quarter"],
                row["area_hectares"],
                row["production_mt"],
                row["farmer_count"],
            ])
        return Response(
            content=buffer.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=makhana-monitoring-snapshot.csv"},
        )
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "summary": summary,
        "report_name": "State and National Monitoring Snapshot",
    }


@app.post("/api/v1/chat/message", response_model=ChatMessageResponse)
def chat_message(payload: ChatMessageRequest, user=Depends(get_optional_user)):
    result = answer_chat(payload.message, payload.page, payload.language, user)
    record = ChatInteractionRecord(
        chat_id=next_chat_id(),
        session_id=payload.session_id,
        user_email=user.email if user else None,
        role=user.role if user else "public",
        page=payload.page,
        language=payload.language,
        message=payload.message,
        answer=result.answer,
        mode=result.mode,
        fallback_used=result.fallback_used,
        source_titles=[item.title for item in result.sources],
        created_at=datetime.now(UTC).isoformat(),
    )
    save_chat_log(record)
    return ChatMessageResponse(
        answer=result.answer,
        sources=[ChatSource(title=item.title, category=item.category, summary=item.summary) for item in result.sources],
        suggested_actions=[ChatAction(label=item["label"], href=item["href"]) for item in result.suggested_actions],
        fallback_used=result.fallback_used,
        mode=result.mode,
    )


def _stream_chunks(text: str, target_size: int = 42) -> list[str]:
    words = text.split()
    chunks: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > target_size:
            chunks.append(current + " ")
            current = word
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks or [text]


@app.post("/api/v1/chat/stream")
def chat_stream(payload: ChatMessageRequest, user=Depends(get_optional_user)):
    result = answer_chat(payload.message, payload.page, payload.language, user)
    record = ChatInteractionRecord(
        chat_id=next_chat_id(),
        session_id=payload.session_id,
        user_email=user.email if user else None,
        role=user.role if user else "public",
        page=payload.page,
        language=payload.language,
        message=payload.message,
        answer=result.answer,
        mode=result.mode,
        fallback_used=result.fallback_used,
        source_titles=[item.title for item in result.sources],
        created_at=datetime.now(UTC).isoformat(),
    )
    save_chat_log(record)

    def event_stream():
        yield json.dumps({"type": "status", "mode": result.mode, "fallback_used": result.fallback_used}) + "\n"
        for chunk in _stream_chunks(result.answer):
            yield json.dumps({"type": "delta", "content": chunk}) + "\n"
        yield json.dumps(
            {
                "type": "complete",
                "sources": [ChatSource(title=item.title, category=item.category, summary=item.summary).model_dump() for item in result.sources],
                "suggested_actions": [ChatAction(label=item["label"], href=item["href"]).model_dump() for item in result.suggested_actions],
                "mode": result.mode,
                "fallback_used": result.fallback_used,
            }
        ) + "\n"

    return StreamingResponse(event_stream(), media_type="application/x-ndjson")


@app.get("/api/v1/chat/history")
def chat_history(limit: int = 20, user=Depends(get_current_user)):
    return [item.model_dump() for item in list_chat_logs(limit=limit, user_email=user.email)]


@app.get("/api/v1/chat/analytics")
def chat_analytics(user=Depends(get_current_user)):
    if user.role != "nmb_admin":
        raise HTTPException(status_code=403, detail="NMB admin only")
    return chat_analytics_snapshot()


@app.get("/")
def home():
    return FileResponse(frontend_dir / "index.html")


@app.get("/login")
def login_page():
    return FileResponse(frontend_dir / "login.html")


@app.get("/services")
def services_page():
    return FileResponse(frontend_dir / "services.html")


@app.get("/schemes")
def schemes_page():
    return FileResponse(frontend_dir / "schemes.html")


@app.get("/updates")
def updates_page():
    return FileResponse(frontend_dir / "updates.html")


@app.get("/helpdesk")
def helpdesk_page():
    return FileResponse(frontend_dir / "helpdesk.html")


@app.get("/dashboard")
def dashboard_page():
    return FileResponse(frontend_dir / "dashboard.html")


@app.get("/beneficiary")
def beneficiary_page():
    return FileResponse(frontend_dir / "beneficiary.html")
