from __future__ import annotations

from pydantic import BaseModel, Field


class User(BaseModel):
    id: str
    name: str
    email: str
    password_hash: str
    role: str
    state_code: str | None = None


class LocationNode(BaseModel):
    code: str
    name: str
    parent_code: str | None = None


class AuditEntry(BaseModel):
    actor: str
    role: str
    action: str
    module: str
    detail: str
    ip_address: str = "unknown"
    timestamp: str = Field(default="")


class NotificationRecord(BaseModel):
    notification_id: str
    event_key: str
    module: str
    recipient: str
    channels: list[str] = Field(default_factory=list)
    subject: str
    message: str
    status: str
    created_at: str
    delivered_at: str | None = None
    provider_results: dict[str, str] = Field(default_factory=dict)


class IntegrationEventRecord(BaseModel):
    event_id: str
    integration_type: str
    provider_name: str
    action: str
    status: str
    request_payload: dict = Field(default_factory=dict)
    response_payload: dict = Field(default_factory=dict)
    created_at: str


class BeneficiaryProfile(BaseModel):
    user_id: str
    name: str
    aadhaar_masked: str
    mobile: str
    email: str
    state_code: str
    district_code: str
    block_code: str
    village_code: str
    cultivation_type: str
    total_land_acres: float
    makhana_area_acres: float
    aadhaar_vault_ref: str | None = None
    identity_verified: bool = False


class DocumentMeta(BaseModel):
    document_id: str
    file_name: str
    document_type: str
    uploaded_at: str


class GeoTag(BaseModel):
    latitude: float
    longitude: float
    accuracy: float
    captured_at: str


class StatusEntry(BaseModel):
    status: str
    remarks: str
    changed_at: str


class ApplicationRecord(BaseModel):
    application_id: str
    beneficiary_user_id: str
    scheme_component: str
    pond_area_acres: float
    requested_amount: float
    current_status: str
    geo_tag: GeoTag | None = None
    documents: list[DocumentMeta] = Field(default_factory=list)
    status_history: list[StatusEntry] = Field(default_factory=list)
    assigned_state_officer: str | None = None
    assigned_inspector: str | None = None
    recommendation_note: str | None = None
    decision_note: str | None = None


class ClarificationRecord(BaseModel):
    clarification_id: str
    application_id: str
    query_text: str
    raised_by: str
    status: str
    response_text: str | None = None
    responded_by: str | None = None
    raised_at: str
    responded_at: str | None = None


class InspectionRecord(BaseModel):
    inspection_id: str
    application_id: str
    inspector_email: str
    assigned_by: str
    status: str
    remarks: str | None = None
    geo_tag: GeoTag | None = None
    photos: list[DocumentMeta] = Field(default_factory=list)
    assigned_at: str
    completed_at: str | None = None


class AnnualActionPlan(BaseModel):
    aap_id: str
    state_code: str
    financial_year: str
    cultivation_target_hectares: float
    farmer_target: int
    infrastructure_target: int
    budget_requested: float
    current_status: str
    submitted_by: str
    submitted_at: str
    remarks: str | None = None
    status_history: list[StatusEntry] = Field(default_factory=list)


class FieldDataRecord(BaseModel):
    field_data_id: str
    state_code: str
    district_code: str
    financial_year: str
    quarter: str
    area_hectares: float
    production_mt: float
    farmer_count: int
    processing_units: int
    entered_by: str
    entered_at: str


class BudgetRecord(BaseModel):
    budget_id: str
    state_code: str
    component_name: str
    financial_year: str
    allocated_amount: float
    released_amount: float
    utilized_amount: float
    updated_by: str
    updated_at: str
    remarks: str | None = None


class ChatInteractionRecord(BaseModel):
    chat_id: str
    session_id: str | None = None
    user_email: str | None = None
    role: str = "public"
    page: str
    language: str = "en"
    message: str
    answer: str
    mode: str
    fallback_used: bool = False
    source_titles: list[str] = Field(default_factory=list)
    created_at: str
