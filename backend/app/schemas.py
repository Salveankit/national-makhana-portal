from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    name: str


class BeneficiaryProfileRequest(BaseModel):
    name: str
    mobile: str
    state_code: str
    district_code: str
    block_code: str
    village_code: str
    cultivation_type: str
    total_land_acres: float
    makhana_area_acres: float


class AadhaarVerificationRequest(BaseModel):
    aadhaar_number: str
    consent: bool


class DocumentRequest(BaseModel):
    file_name: str
    document_type: str


class GeoTagRequest(BaseModel):
    latitude: float
    longitude: float
    accuracy: float


class ApplicationRequest(BaseModel):
    scheme_component: str
    pond_area_acres: float
    requested_amount: float
    documents: list[DocumentRequest] = []
    geo_tag: GeoTagRequest | None = None


class ClarificationRequest(BaseModel):
    query_text: str


class ClarificationResponseRequest(BaseModel):
    response_text: str


class InspectionAssignRequest(BaseModel):
    inspector_email: str


class InspectionCompleteRequest(BaseModel):
    remarks: str
    latitude: float
    longitude: float
    accuracy: float
    photo_name: str


class RecommendationRequest(BaseModel):
    remarks: str


class DecisionRequest(BaseModel):
    decision: str
    remarks: str


class BatchDecisionRequest(BaseModel):
    application_ids: list[str]
    decision: str
    remarks: str


class AAPRequest(BaseModel):
    financial_year: str
    cultivation_target_hectares: float
    farmer_target: int
    infrastructure_target: int
    budget_requested: float
    remarks: str


class AAPReviewRequest(BaseModel):
    decision: str
    remarks: str


class FieldDataRequest(BaseModel):
    district_code: str
    financial_year: str
    quarter: str
    area_hectares: float
    production_mt: float
    farmer_count: int
    processing_units: int


class BudgetRequest(BaseModel):
    state_code: str
    component_name: str
    financial_year: str
    allocated_amount: float
    released_amount: float
    utilized_amount: float


class BudgetUtilizationRequest(BaseModel):
    released_amount: float
    utilized_amount: float
    remarks: str


class MockNotificationRequest(BaseModel):
    channel: str
    recipient: str
    template_key: str
    message: str


class MockAadhaarKycRequest(BaseModel):
    beneficiary_name: str
    aadhaar_number: str
    consent: bool


class MockDBTRequest(BaseModel):
    application_id: str
    beneficiary_name: str
    bank_account_last4: str
    amount: float
