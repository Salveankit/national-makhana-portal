from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock
from typing import Any

from backend.app.core.config import settings
from backend.app.core.security import hash_password
from backend.app.models import (
    AnnualActionPlan,
    ApplicationRecord,
    AuditEntry,
    BeneficiaryProfile,
    BudgetRecord,
    ClarificationRecord,
    DocumentMeta,
    FieldDataRecord,
    GeoTag,
    IntegrationEventRecord,
    InspectionRecord,
    LocationNode,
    NotificationRecord,
    StatusEntry,
    User,
)

DB_LOCK = Lock()
DB_PATH = Path(settings.sqlite_path)
DOCUMENT_ROOT = Path(settings.document_root)


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _serialize(model: Any) -> str:
    if hasattr(model, "model_dump_json"):
        return model.model_dump_json()
    return json.dumps(model)


def _deserialize(row: sqlite3.Row | None, model_cls):
    if row is None:
        return None
    return model_cls.model_validate_json(row["payload"])


def _deserialize_many(rows: list[sqlite3.Row], model_cls):
    return [model_cls.model_validate_json(row["payload"]) for row in rows]


def init_storage() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOCUMENT_ROOT.mkdir(parents=True, exist_ok=True)
    with DB_LOCK:
        conn = _connect()
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                role TEXT NOT NULL,
                state_code TEXT
            );
            CREATE TABLE IF NOT EXISTS locations (
                code TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                parent_code TEXT,
                location_type TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS beneficiary_profiles (
                user_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                state_code TEXT NOT NULL,
                district_code TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS applications (
                application_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                beneficiary_user_id TEXT NOT NULL,
                current_status TEXT NOT NULL,
                assigned_state_officer TEXT,
                assigned_inspector TEXT
            );
            CREATE TABLE IF NOT EXISTS clarifications (
                clarification_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                application_id TEXT NOT NULL,
                status TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS inspections (
                inspection_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                application_id TEXT NOT NULL,
                inspector_email TEXT NOT NULL,
                status TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS annual_action_plans (
                aap_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                state_code TEXT NOT NULL,
                submitted_by TEXT NOT NULL,
                current_status TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS field_data (
                field_data_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                state_code TEXT NOT NULL,
                district_code TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS budgets (
                budget_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                state_code TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payload TEXT NOT NULL,
                module TEXT NOT NULL,
                actor TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS notifications (
                notification_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                module TEXT NOT NULL,
                recipient TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS integration_events (
                event_id TEXT PRIMARY KEY,
                payload TEXT NOT NULL,
                integration_type TEXT NOT NULL,
                provider_name TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )
        conn.commit()
        conn.close()
    seed_if_empty()


def seed_if_empty() -> None:
    with DB_LOCK:
        conn = _connect()
        has_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0
        if not has_users:
            _seed_demo_data(conn)
            conn.commit()
        conn.close()


def _seed_demo_data(conn: sqlite3.Connection) -> None:
    users = [
        User(id="u1", name="NMB Admin", email="nmb.admin@example.com", password_hash=hash_password("Pass@123"), role="nmb_admin"),
        User(id="u2", name="Bihar Officer", email="bihar.officer@example.com", password_hash=hash_password("Pass@123"), role="state_officer", state_code="BR"),
        User(id="u3", name="District Inspector", email="inspector@example.com", password_hash=hash_password("Pass@123"), role="inspector", state_code="BR"),
        User(id="u4", name="Demo Farmer", email="farmer@example.com", password_hash=hash_password("Pass@123"), role="beneficiary", state_code="BR"),
    ]
    locations = [
        ("state", LocationNode(code="BR", name="Bihar")),
        ("state", LocationNode(code="WB", name="West Bengal")),
        ("state", LocationNode(code="OD", name="Odisha")),
        ("district", LocationNode(code="BR-PUR", name="Purnia", parent_code="BR")),
        ("district", LocationNode(code="BR-KAT", name="Katihar", parent_code="BR")),
        ("district", LocationNode(code="BR-AR", name="Araria", parent_code="BR")),
        ("block", LocationNode(code="BR-PUR-KR", name="Krityanand Nagar", parent_code="BR-PUR")),
        ("block", LocationNode(code="BR-KAT-KD", name="Kadwa", parent_code="BR-KAT")),
        ("village", LocationNode(code="BR-PUR-KR-001", name="Majra", parent_code="BR-PUR-KR")),
        ("village", LocationNode(code="BR-KAT-KD-001", name="Durgaganj", parent_code="BR-KAT-KD")),
    ]
    beneficiary_profile = BeneficiaryProfile(
        user_id="u4",
        name="Demo Farmer",
        aadhaar_masked="XXXX-XXXX-1234",
        mobile="9876543210",
        email="farmer@example.com",
        state_code="BR",
        district_code="BR-PUR",
        block_code="BR-PUR-KR",
        village_code="BR-PUR-KR-001",
        cultivation_type="pond_based",
        total_land_acres=3.5,
        makhana_area_acres=1.8,
        aadhaar_vault_ref="vault-u4-1234",
        identity_verified=True,
    )
    now = _utc_now()
    applications = [
        ApplicationRecord(
            application_id="APP-BR-0001",
            beneficiary_user_id="u4",
            scheme_component="Makhana Cultivation Support",
            pond_area_acres=1.5,
            requested_amount=50000,
            current_status="Submitted",
            assigned_state_officer="bihar.officer@example.com",
            geo_tag=GeoTag(latitude=25.7773, longitude=87.4753, accuracy=18, captured_at=now),
            documents=[DocumentMeta(document_id="APP-BR-0001-DOC-1", file_name="land-record.pdf", document_type="land_record", uploaded_at=now)],
            status_history=[
                StatusEntry(status="Submitted", remarks="Fresh application awaiting state review", changed_at=now),
                StatusEntry(status="Draft", remarks="Application drafted by beneficiary", changed_at=now),
            ],
        ),
        ApplicationRecord(
            application_id="APP-BR-0002",
            beneficiary_user_id="u4",
            scheme_component="Processing Unit Support",
            pond_area_acres=0.8,
            requested_amount=120000,
            current_status="Clarification Raised",
            assigned_state_officer="bihar.officer@example.com",
            geo_tag=GeoTag(latitude=25.7901, longitude=87.4611, accuracy=15, captured_at=now),
            documents=[DocumentMeta(document_id="APP-BR-0002-DOC-1", file_name="processing-plan.pdf", document_type="identity_proof", uploaded_at=now)],
            status_history=[
                StatusEntry(status="Clarification Raised", remarks="Need clearer processing unit estimate", changed_at=now),
                StatusEntry(status="Under State Review", remarks="State officer started review", changed_at=now),
                StatusEntry(status="Submitted", remarks="Application submitted successfully", changed_at=now),
            ],
        ),
        ApplicationRecord(
            application_id="APP-BR-0003",
            beneficiary_user_id="u4",
            scheme_component="Training and Extension Support",
            pond_area_acres=1.1,
            requested_amount=35000,
            current_status="Inspection Assigned",
            assigned_state_officer="bihar.officer@example.com",
            assigned_inspector="inspector@example.com",
            geo_tag=GeoTag(latitude=25.7551, longitude=87.5022, accuracy=10, captured_at=now),
            documents=[DocumentMeta(document_id="APP-BR-0003-DOC-1", file_name="training-request.pdf", document_type="bank_proof", uploaded_at=now)],
            status_history=[
                StatusEntry(status="Inspection Assigned", remarks="Field visit assigned to district inspector", changed_at=now),
                StatusEntry(status="Under State Review", remarks="State officer review completed", changed_at=now),
                StatusEntry(status="Submitted", remarks="Application submitted successfully", changed_at=now),
            ],
        ),
        ApplicationRecord(
            application_id="APP-BR-0004",
            beneficiary_user_id="u4",
            scheme_component="Makhana Cultivation Support",
            pond_area_acres=2.0,
            requested_amount=78000,
            current_status="Recommended by State",
            assigned_state_officer="bihar.officer@example.com",
            assigned_inspector="inspector@example.com",
            geo_tag=GeoTag(latitude=25.8125, longitude=87.4312, accuracy=11, captured_at=now),
            documents=[DocumentMeta(document_id="APP-BR-0004-DOC-1", file_name="site-photo.pdf", document_type="land_record", uploaded_at=now)],
            status_history=[
                StatusEntry(status="Recommended by State", remarks="Eligible and forwarded to NMB", changed_at=now),
                StatusEntry(status="Inspection Completed", remarks="Site verified by district inspector", changed_at=now),
                StatusEntry(status="Inspection Assigned", remarks="Field visit assigned", changed_at=now),
                StatusEntry(status="Submitted", remarks="Application submitted successfully", changed_at=now),
            ],
        ),
        ApplicationRecord(
            application_id="APP-BR-0005",
            beneficiary_user_id="u4",
            scheme_component="Infrastructure Support",
            pond_area_acres=1.7,
            requested_amount=150000,
            current_status="Approved",
            assigned_state_officer="bihar.officer@example.com",
            assigned_inspector="inspector@example.com",
            geo_tag=GeoTag(latitude=25.7682, longitude=87.4784, accuracy=9, captured_at=now),
            documents=[DocumentMeta(document_id="APP-BR-0005-DOC-1", file_name="infrastructure-layout.pdf", document_type="land_record", uploaded_at=now)],
            status_history=[
                StatusEntry(status="Approved", remarks="Approved by NMB for release readiness", changed_at=now),
                StatusEntry(status="Recommended by State", remarks="State recommendation completed", changed_at=now),
                StatusEntry(status="Inspection Completed", remarks="Site verified successfully", changed_at=now),
                StatusEntry(status="Submitted", remarks="Application submitted successfully", changed_at=now),
            ],
        ),
    ]
    clarifications = [
        ClarificationRecord(
            clarification_id="CLR-0001",
            application_id="APP-BR-0002",
            query_text="Please upload clearer processing unit estimate and cost breakup.",
            raised_by="bihar.officer@example.com",
            status="Open",
            raised_at=now,
        )
    ]
    inspections = [
        InspectionRecord(
            inspection_id="INSP-0001",
            application_id="APP-BR-0003",
            inspector_email="inspector@example.com",
            assigned_by="bihar.officer@example.com",
            status="Assigned",
            assigned_at=now,
        ),
        InspectionRecord(
            inspection_id="INSP-0002",
            application_id="APP-BR-0004",
            inspector_email="inspector@example.com",
            assigned_by="bihar.officer@example.com",
            status="Completed",
            remarks="Cultivation site verified with geo-tagged evidence.",
            geo_tag=GeoTag(latitude=25.8125, longitude=87.4312, accuracy=8, captured_at=now),
            photos=[DocumentMeta(document_id="INSP-0002-PHOTO-1", file_name="inspection-app4.jpg", document_type="inspection_photo", uploaded_at=now)],
            assigned_at=now,
            completed_at=now,
        ),
        InspectionRecord(
            inspection_id="INSP-0003",
            application_id="APP-BR-0005",
            inspector_email="inspector@example.com",
            assigned_by="bihar.officer@example.com",
            status="Completed",
            remarks="Infrastructure readiness checked and validated.",
            geo_tag=GeoTag(latitude=25.7682, longitude=87.4784, accuracy=7, captured_at=now),
            photos=[DocumentMeta(document_id="INSP-0003-PHOTO-1", file_name="inspection-app5.jpg", document_type="inspection_photo", uploaded_at=now)],
            assigned_at=now,
            completed_at=now,
        ),
    ]
    aap = AnnualActionPlan(
        aap_id="AAP-BR-2026",
        state_code="BR",
        financial_year="2026-27",
        cultivation_target_hectares=1250,
        farmer_target=4800,
        infrastructure_target=24,
        budget_requested=22500000,
        current_status="Submitted",
        submitted_by="bihar.officer@example.com",
        submitted_at=now,
        remarks="Focus on Purnia, Katihar, and Araria clusters.",
        status_history=[
            StatusEntry(status="Draft", remarks="Initial planning prepared by Bihar state office", changed_at=now),
            StatusEntry(status="Submitted", remarks="Submitted for NMB review", changed_at=now),
        ],
    )
    approved_aap = AnnualActionPlan(
        aap_id="AAP-BR-2027",
        state_code="BR",
        financial_year="2027-28",
        cultivation_target_hectares=1450,
        farmer_target=5400,
        infrastructure_target=30,
        budget_requested=25500000,
        current_status="Approved",
        submitted_by="bihar.officer@example.com",
        submitted_at=now,
        remarks="Approved expansion plan for high-yield districts.",
        status_history=[
            StatusEntry(status="Approved", remarks="Approved by NMB for next FY rollout", changed_at=now),
            StatusEntry(status="Submitted", remarks="Submitted for NMB review", changed_at=now),
            StatusEntry(status="Draft", remarks="Initial planning prepared by Bihar state office", changed_at=now),
        ],
    )
    field_rows = [
        FieldDataRecord(
            field_data_id="FD-001",
            state_code="BR",
            district_code="BR-PUR",
            financial_year="2026-27",
            quarter="Q1",
            area_hectares=420,
            production_mt=860,
            farmer_count=1600,
            processing_units=7,
            entered_by="bihar.officer@example.com",
            entered_at=now,
        ),
        FieldDataRecord(
            field_data_id="FD-002",
            state_code="BR",
            district_code="BR-KAT",
            financial_year="2026-27",
            quarter="Q1",
            area_hectares=310,
            production_mt=620,
            farmer_count=1180,
            processing_units=5,
            entered_by="bihar.officer@example.com",
            entered_at=now,
        ),
    ]
    budget_rows = [
        BudgetRecord(
            budget_id="BUD-BR-01",
            state_code="BR",
            component_name="Cultivation Support",
            financial_year="2026-27",
            allocated_amount=18000000,
            released_amount=12000000,
            utilized_amount=7600000,
            updated_by="nmb.admin@example.com",
            updated_at=now,
            remarks="Initial allocation for cultivation support",
        ),
        BudgetRecord(
            budget_id="BUD-BR-02",
            state_code="BR",
            component_name="Processing Infrastructure",
            financial_year="2026-27",
            allocated_amount=9000000,
            released_amount=4500000,
            utilized_amount=2400000,
            updated_by="nmb.admin@example.com",
            updated_at=now,
            remarks="Initial allocation for processing infrastructure",
        ),
        BudgetRecord(
            budget_id="BUD-BR-03",
            state_code="BR",
            component_name="Training and Extension",
            financial_year="2026-27",
            allocated_amount=3500000,
            released_amount=2200000,
            utilized_amount=1250000,
            updated_by="bihar.officer@example.com",
            updated_at=now,
            remarks="Utilization updated after Q2 field review",
        ),
    ]
    notifications = [
        NotificationRecord(
            notification_id="NTF-0001",
            event_key="application.submitted",
            module="application",
            recipient="farmer@example.com",
            channels=["in_app", "email", "sms"],
            subject="Application submitted",
            message="Application APP-BR-0001 has been submitted.",
            status="logged",
            created_at=now,
            delivered_at=now,
            provider_results={"in_app": "logged", "email": "delivered", "sms": "awaiting_credentials"},
        ),
        NotificationRecord(
            notification_id="NTF-0002",
            event_key="inspection.assigned",
            module="inspection",
            recipient="inspector@example.com",
            channels=["in_app", "email"],
            subject="Inspection assigned",
            message="Inspection INSP-0001 has been assigned.",
            status="logged",
            created_at=now,
            delivered_at=now,
            provider_results={"in_app": "logged", "email": "delivered"},
        ),
        NotificationRecord(
            notification_id="NTF-0003",
            event_key="aap.approved",
            module="aap",
            recipient="bihar.officer@example.com",
            channels=["in_app", "email"],
            subject="AAP Approved",
            message="AAP-BR-2027 has been approved.",
            status="logged",
            created_at=now,
            delivered_at=now,
            provider_results={"in_app": "logged", "email": "delivered"},
        ),
    ]
    integration_events = [
        IntegrationEventRecord(
            event_id="INT-0001",
            integration_type="notification",
            provider_name="mock-sms-gateway",
            action="send_template_message",
            status="ready_for_live_swap",
            request_payload={"channel": "sms", "template_key": "application_submitted"},
            response_payload={"provider_reference": "mock-sms-gateway-001", "delivery_state": "ready_for_live_swap"},
            created_at=now,
        ),
        IntegrationEventRecord(
            event_id="INT-0002",
            integration_type="identity",
            provider_name="mock-aadhaar-vault",
            action="kyc_verify",
            status="mock_mode",
            request_payload={"beneficiary_name": "Demo Farmer", "aadhaar_masked": "XXXX-XXXX-1234"},
            response_payload={"verification_status": "verified", "vault_reference": "vault-u4-1234"},
            created_at=now,
        ),
        IntegrationEventRecord(
            event_id="INT-0003",
            integration_type="payments",
            provider_name="mock-dbt-switch",
            action="disburse",
            status="banking_integration_pending",
            request_payload={"application_id": "APP-BR-0005", "amount": 150000},
            response_payload={"disbursement_reference": "DBT-DEMO-0001", "transaction_status": "queued_for_department_approval"},
            created_at=now,
        ),
    ]

    conn.executemany(
        "INSERT INTO users(email, payload, role, state_code) VALUES (?, ?, ?, ?)",
        [(user.email, _serialize(user), user.role, user.state_code) for user in users],
    )
    conn.executemany(
        "INSERT INTO locations(code, payload, parent_code, location_type) VALUES (?, ?, ?, ?)",
        [(node.code, _serialize(node), node.parent_code, location_type) for location_type, node in locations],
    )
    conn.execute(
        "INSERT INTO beneficiary_profiles(user_id, payload, state_code, district_code) VALUES (?, ?, ?, ?)",
        (
            beneficiary_profile.user_id,
            _serialize(beneficiary_profile),
            beneficiary_profile.state_code,
            beneficiary_profile.district_code,
        ),
    )
    conn.executemany(
        "INSERT INTO applications(application_id, payload, beneficiary_user_id, current_status, assigned_state_officer, assigned_inspector) VALUES (?, ?, ?, ?, ?, ?)",
        [
            (
                application.application_id,
                _serialize(application),
                application.beneficiary_user_id,
                application.current_status,
                application.assigned_state_officer,
                application.assigned_inspector,
            )
            for application in applications
        ],
    )
    conn.executemany(
        "INSERT INTO clarifications(clarification_id, payload, application_id, status) VALUES (?, ?, ?, ?)",
        [(item.clarification_id, _serialize(item), item.application_id, item.status) for item in clarifications],
    )
    conn.executemany(
        "INSERT INTO inspections(inspection_id, payload, application_id, inspector_email, status) VALUES (?, ?, ?, ?, ?)",
        [(item.inspection_id, _serialize(item), item.application_id, item.inspector_email, item.status) for item in inspections],
    )
    conn.executemany(
        "INSERT INTO annual_action_plans(aap_id, payload, state_code, submitted_by, current_status) VALUES (?, ?, ?, ?, ?)",
        [
            (item.aap_id, _serialize(item), item.state_code, item.submitted_by, item.current_status)
            for item in [aap, approved_aap]
        ],
    )
    conn.executemany(
        "INSERT INTO field_data(field_data_id, payload, state_code, district_code) VALUES (?, ?, ?, ?)",
        [(row.field_data_id, _serialize(row), row.state_code, row.district_code) for row in field_rows],
    )
    conn.executemany(
        "INSERT INTO budgets(budget_id, payload, state_code) VALUES (?, ?, ?)",
        [(row.budget_id, _serialize(row), row.state_code) for row in budget_rows],
    )
    conn.executemany(
        "INSERT INTO notifications(notification_id, payload, module, recipient, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        [(item.notification_id, _serialize(item), item.module, item.recipient, item.status, item.created_at) for item in notifications],
    )
    conn.executemany(
        "INSERT INTO integration_events(event_id, payload, integration_type, provider_name, status, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        [(item.event_id, _serialize(item), item.integration_type, item.provider_name, item.status, item.created_at) for item in integration_events],
    )


def reset_demo_dataset() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOCUMENT_ROOT.mkdir(parents=True, exist_ok=True)
    for child in DOCUMENT_ROOT.iterdir():
        if child.is_file():
            child.unlink()
    with DB_LOCK:
        conn = _connect()
        conn.executescript(
            """
            DELETE FROM integration_events;
            DELETE FROM notifications;
            DELETE FROM audit_logs;
            DELETE FROM budgets;
            DELETE FROM field_data;
            DELETE FROM annual_action_plans;
            DELETE FROM inspections;
            DELETE FROM clarifications;
            DELETE FROM applications;
            DELETE FROM beneficiary_profiles;
            DELETE FROM locations;
            DELETE FROM users;
            """
        )
        _seed_demo_data(conn)
        conn.commit()
        conn.close()


def storage_health() -> dict[str, str]:
    status = {
        "sqlite": "down",
        "documents": "down",
        "postgres": "configured",
        "redis": "configured",
        "minio": "configured",
    }
    try:
        with DB_LOCK:
            conn = _connect()
            conn.execute("SELECT 1").fetchone()
            conn.close()
        status["sqlite"] = "up"
    except Exception:
        status["sqlite"] = "down"

    try:
        DOCUMENT_ROOT.mkdir(parents=True, exist_ok=True)
        probe = DOCUMENT_ROOT / ".healthcheck"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        status["documents"] = "up"
    except Exception:
        status["documents"] = "down"
    return status


def get_user_by_email(email: str) -> User | None:
    with DB_LOCK:
        conn = _connect()
        row = conn.execute("SELECT payload FROM users WHERE email = ?", (email,)).fetchone()
        conn.close()
    return _deserialize(row, User)


def get_user_by_id(user_id: str) -> User | None:
    with DB_LOCK:
        conn = _connect()
        row = conn.execute("SELECT payload FROM users").fetchall()
        conn.close()
    users = _deserialize_many(row, User)
    return next((user for user in users if user.id == user_id), None)


def list_locations(location_type: str, parent_code: str | None = None) -> list[LocationNode]:
    query = "SELECT payload FROM locations WHERE location_type = ?"
    params: list[Any] = [location_type]
    if parent_code is None:
        query += " AND parent_code IS NULL"
    else:
        query += " AND parent_code = ?"
        params.append(parent_code)
    with DB_LOCK:
        conn = _connect()
        rows = conn.execute(query, params).fetchall()
        conn.close()
    return _deserialize_many(rows, LocationNode)


def add_audit(actor: str, role: str, action: str, module: str, detail: str, ip_address: str = "unknown") -> None:
    entry = AuditEntry(
        actor=actor,
        role=role,
        action=action,
        module=module,
        detail=detail,
        ip_address=ip_address,
        timestamp=_utc_now(),
    )
    with DB_LOCK:
        conn = _connect()
        conn.execute(
            "INSERT INTO audit_logs(payload, module, actor, created_at) VALUES (?, ?, ?, ?)",
            (_serialize(entry), module, actor, entry.timestamp),
        )
        conn.commit()
        conn.close()


def list_audit_logs(limit: int = 100) -> list[AuditEntry]:
    with DB_LOCK:
        conn = _connect()
        rows = conn.execute(
            "SELECT payload FROM audit_logs ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        conn.close()
    return _deserialize_many(rows, AuditEntry)


def next_notification_id() -> str:
    return _next_id("NTF", "notifications")


def next_integration_event_id() -> str:
    return _next_id("INT", "integration_events")


def save_notification(record: NotificationRecord) -> NotificationRecord:
    with DB_LOCK:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO notifications(notification_id, payload, module, recipient, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(notification_id) DO UPDATE SET
              payload = excluded.payload,
              status = excluded.status
            """,
            (record.notification_id, _serialize(record), record.module, record.recipient, record.status, record.created_at),
        )
        conn.commit()
        conn.close()
    return record


def list_notifications(limit: int = 100, recipient: str | None = None) -> list[NotificationRecord]:
    query = "SELECT payload FROM notifications"
    params: list[Any] = []
    if recipient:
        query += " WHERE recipient = ?"
        params.append(recipient)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    with DB_LOCK:
        conn = _connect()
        rows = conn.execute(query, params).fetchall()
        conn.close()
    return _deserialize_many(rows, NotificationRecord)


def save_integration_event(record: IntegrationEventRecord) -> IntegrationEventRecord:
    with DB_LOCK:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO integration_events(event_id, payload, integration_type, provider_name, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(event_id) DO UPDATE SET
              payload = excluded.payload,
              status = excluded.status
            """,
            (
                record.event_id,
                _serialize(record),
                record.integration_type,
                record.provider_name,
                record.status,
                record.created_at,
            ),
        )
        conn.commit()
        conn.close()
    return record


def list_integration_events(limit: int = 100, integration_type: str | None = None) -> list[IntegrationEventRecord]:
    query = "SELECT payload FROM integration_events"
    params: list[Any] = []
    if integration_type:
        query += " WHERE integration_type = ?"
        params.append(integration_type)
    query += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)
    with DB_LOCK:
        conn = _connect()
        rows = conn.execute(query, params).fetchall()
        conn.close()
    return _deserialize_many(rows, IntegrationEventRecord)


def get_beneficiary_profile(user_id: str) -> BeneficiaryProfile | None:
    with DB_LOCK:
        conn = _connect()
        row = conn.execute("SELECT payload FROM beneficiary_profiles WHERE user_id = ?", (user_id,)).fetchone()
        conn.close()
    return _deserialize(row, BeneficiaryProfile)


def save_beneficiary_profile(profile: BeneficiaryProfile) -> BeneficiaryProfile:
    with DB_LOCK:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO beneficiary_profiles(user_id, payload, state_code, district_code)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
              payload = excluded.payload,
              state_code = excluded.state_code,
              district_code = excluded.district_code
            """,
            (profile.user_id, _serialize(profile), profile.state_code, profile.district_code),
        )
        conn.commit()
        conn.close()
    return profile


def _store_document_placeholder(document_id: str, file_name: str) -> None:
    target = DOCUMENT_ROOT / f"{document_id}-{file_name}"
    target.write_text(f"placeholder document record for {file_name}\n", encoding="utf-8")


def _application_row(record: ApplicationRecord) -> tuple[Any, ...]:
    return (
        record.application_id,
        _serialize(record),
        record.beneficiary_user_id,
        record.current_status,
        record.assigned_state_officer,
        record.assigned_inspector,
    )


def _clarification_row(record: ClarificationRecord) -> tuple[Any, ...]:
    return (record.clarification_id, _serialize(record), record.application_id, record.status)


def _inspection_row(record: InspectionRecord) -> tuple[Any, ...]:
    return (record.inspection_id, _serialize(record), record.application_id, record.inspector_email, record.status)


def list_beneficiary_applications(user_id: str) -> list[ApplicationRecord]:
    with DB_LOCK:
        conn = _connect()
        rows = conn.execute(
            "SELECT payload FROM applications WHERE beneficiary_user_id = ? ORDER BY application_id DESC",
            (user_id,),
        ).fetchall()
        conn.close()
    return _deserialize_many(rows, ApplicationRecord)


def get_application(application_id: str) -> ApplicationRecord | None:
    with DB_LOCK:
        conn = _connect()
        row = conn.execute("SELECT payload FROM applications WHERE application_id = ?", (application_id,)).fetchone()
        conn.close()
    return _deserialize(row, ApplicationRecord)


def _next_id(prefix: str, table_name: str, state_code: str | None = None) -> str:
    with DB_LOCK:
        conn = _connect()
        count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0] + 1
        conn.close()
    if prefix == "APP":
        return f"APP-{state_code}-{count:04d}"
    if prefix == "CLR":
        return f"CLR-{count:04d}"
    if prefix == "INSP":
        return f"INSP-{count:04d}"
    if prefix == "FD":
        return f"FD-{count:03d}"
    if prefix == "BUD":
        return f"BUD-{state_code}-{count:02d}"
    if prefix == "NTF":
        return f"NTF-{count:04d}"
    if prefix == "INT":
        return f"INT-{count:04d}"
    return f"{prefix}-{count:04d}"


def next_application_id(state_code: str) -> str:
    return _next_id("APP", "applications", state_code)


def next_clarification_id() -> str:
    return _next_id("CLR", "clarifications")


def next_inspection_id() -> str:
    return _next_id("INSP", "inspections")


def next_aap_id(state_code: str, financial_year: str) -> str:
    return f"AAP-{state_code}-{financial_year.split('-')[0]}"


def next_field_data_id() -> str:
    return _next_id("FD", "field_data")


def next_budget_id(state_code: str) -> str:
    return _next_id("BUD", "budgets", state_code)


def create_application(record: ApplicationRecord) -> ApplicationRecord:
    for document in record.documents:
        _store_document_placeholder(document.document_id, document.file_name)
    with DB_LOCK:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO applications(application_id, payload, beneficiary_user_id, current_status, assigned_state_officer, assigned_inspector)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            _application_row(record),
        )
        conn.commit()
        conn.close()
    return record


def save_application(record: ApplicationRecord) -> ApplicationRecord:
    with DB_LOCK:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO applications(application_id, payload, beneficiary_user_id, current_status, assigned_state_officer, assigned_inspector)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(application_id) DO UPDATE SET
              payload = excluded.payload,
              current_status = excluded.current_status,
              assigned_state_officer = excluded.assigned_state_officer,
              assigned_inspector = excluded.assigned_inspector
            """,
            _application_row(record),
        )
        conn.commit()
        conn.close()
    return record


def get_open_clarification(application_id: str) -> ClarificationRecord | None:
    with DB_LOCK:
        conn = _connect()
        row = conn.execute(
            "SELECT payload FROM clarifications WHERE application_id = ? AND status = 'Open' ORDER BY clarification_id DESC LIMIT 1",
            (application_id,),
        ).fetchone()
        conn.close()
    return _deserialize(row, ClarificationRecord)


def save_clarification(record: ClarificationRecord) -> ClarificationRecord:
    with DB_LOCK:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO clarifications(clarification_id, payload, application_id, status)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(clarification_id) DO UPDATE SET
              payload = excluded.payload,
              status = excluded.status
            """,
            _clarification_row(record),
        )
        conn.commit()
        conn.close()
    return record


def list_clarifications(application_ids: set[str] | None = None) -> list[ClarificationRecord]:
    query = "SELECT payload FROM clarifications"
    params: list[Any] = []
    if application_ids:
        placeholders = ",".join("?" for _ in application_ids)
        query += f" WHERE application_id IN ({placeholders})"
        params.extend(sorted(application_ids))
    query += " ORDER BY clarification_id DESC"
    with DB_LOCK:
        conn = _connect()
        rows = conn.execute(query, params).fetchall()
        conn.close()
    return _deserialize_many(rows, ClarificationRecord)


def save_inspection(record: InspectionRecord) -> InspectionRecord:
    with DB_LOCK:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO inspections(inspection_id, payload, application_id, inspector_email, status)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(inspection_id) DO UPDATE SET
              payload = excluded.payload,
              inspector_email = excluded.inspector_email,
              status = excluded.status
            """,
            _inspection_row(record),
        )
        conn.commit()
        conn.close()
    return record


def get_inspection(inspection_id: str) -> InspectionRecord | None:
    with DB_LOCK:
        conn = _connect()
        row = conn.execute("SELECT payload FROM inspections WHERE inspection_id = ?", (inspection_id,)).fetchone()
        conn.close()
    return _deserialize(row, InspectionRecord)


def list_inspections(role: str, user_email: str) -> list[InspectionRecord]:
    query = "SELECT payload FROM inspections"
    params: list[Any] = []
    if role == "inspector":
        query += " WHERE inspector_email = ?"
        params.append(user_email)
    query += " ORDER BY inspection_id DESC"
    with DB_LOCK:
        conn = _connect()
        rows = conn.execute(query, params).fetchall()
        conn.close()
    return _deserialize_many(rows, InspectionRecord)


def list_officer_applications(role: str, user_email: str) -> list[ApplicationRecord]:
    query = "SELECT payload FROM applications"
    params: list[Any] = []
    if role in {"state_officer", "inspector"}:
        query += " WHERE assigned_state_officer = ? OR assigned_inspector = ?"
        params.extend([user_email, user_email])
    query += " ORDER BY application_id DESC"
    with DB_LOCK:
        conn = _connect()
        rows = conn.execute(query, params).fetchall()
        conn.close()
    return _deserialize_many(rows, ApplicationRecord)


def get_aap(aap_id: str) -> AnnualActionPlan | None:
    with DB_LOCK:
        conn = _connect()
        row = conn.execute("SELECT payload FROM annual_action_plans WHERE aap_id = ?", (aap_id,)).fetchone()
        conn.close()
    return _deserialize(row, AnnualActionPlan)


def list_aap(
    role: str,
    user_email: str,
    state_code: str | None,
    financial_year: str | None = None,
    current_status: str | None = None,
) -> list[AnnualActionPlan]:
    query = "SELECT payload FROM annual_action_plans"
    params: list[Any] = []
    if role == "state_officer":
        query += " WHERE submitted_by = ? OR state_code = ?"
        params.extend([user_email, state_code])
    query += " ORDER BY aap_id DESC"
    with DB_LOCK:
        conn = _connect()
        rows = conn.execute(query, params).fetchall()
        conn.close()
    records = _deserialize_many(rows, AnnualActionPlan)
    if financial_year:
        records = [item for item in records if item.financial_year == financial_year]
    if current_status:
        records = [item for item in records if item.current_status == current_status]
    return records


def save_aap(record: AnnualActionPlan) -> AnnualActionPlan:
    with DB_LOCK:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO annual_action_plans(aap_id, payload, state_code, submitted_by, current_status)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(aap_id) DO UPDATE SET
              payload = excluded.payload,
              current_status = excluded.current_status
            """,
            (record.aap_id, _serialize(record), record.state_code, record.submitted_by, record.current_status),
        )
        conn.commit()
        conn.close()
    return record


def list_field_data(
    role: str,
    state_code: str | None,
    district_code: str | None = None,
    financial_year: str | None = None,
    quarter: str | None = None,
) -> list[FieldDataRecord]:
    query = "SELECT payload FROM field_data"
    params: list[Any] = []
    if role == "state_officer":
        query += " WHERE state_code = ?"
        params.append(state_code)
    query += " ORDER BY field_data_id DESC"
    with DB_LOCK:
        conn = _connect()
        rows = conn.execute(query, params).fetchall()
        conn.close()
    records = _deserialize_many(rows, FieldDataRecord)
    if district_code:
        records = [item for item in records if item.district_code == district_code]
    if financial_year:
        records = [item for item in records if item.financial_year == financial_year]
    if quarter:
        records = [item for item in records if item.quarter == quarter]
    return records


def save_field_data(record: FieldDataRecord) -> FieldDataRecord:
    with DB_LOCK:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO field_data(field_data_id, payload, state_code, district_code)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(field_data_id) DO UPDATE SET
              payload = excluded.payload
            """,
            (record.field_data_id, _serialize(record), record.state_code, record.district_code),
        )
        conn.commit()
        conn.close()
    return record


def get_budget(budget_id: str) -> BudgetRecord | None:
    with DB_LOCK:
        conn = _connect()
        row = conn.execute("SELECT payload FROM budgets WHERE budget_id = ?", (budget_id,)).fetchone()
        conn.close()
    return _deserialize(row, BudgetRecord)


def list_budgets(
    role: str,
    state_code: str | None,
    financial_year: str | None = None,
    component_name: str | None = None,
) -> list[BudgetRecord]:
    query = "SELECT payload FROM budgets"
    params: list[Any] = []
    if role == "state_officer":
        query += " WHERE state_code = ?"
        params.append(state_code)
    query += " ORDER BY budget_id DESC"
    with DB_LOCK:
        conn = _connect()
        rows = conn.execute(query, params).fetchall()
        conn.close()
    records = _deserialize_many(rows, BudgetRecord)
    if financial_year:
        records = [item for item in records if item.financial_year == financial_year]
    if component_name:
        records = [item for item in records if item.component_name == component_name]
    return records


def save_budget(record: BudgetRecord) -> BudgetRecord:
    with DB_LOCK:
        conn = _connect()
        conn.execute(
            """
            INSERT INTO budgets(budget_id, payload, state_code)
            VALUES (?, ?, ?)
            ON CONFLICT(budget_id) DO UPDATE SET
              payload = excluded.payload
            """,
            (record.budget_id, _serialize(record), record.state_code),
        )
        conn.commit()
        conn.close()
    return record


init_storage()
