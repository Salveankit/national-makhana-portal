import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


class WorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def login(self, email: str, password: str = "Pass@123") -> str:
        response = self.client.post("/api/v1/auth/login", json={"email": email, "password": password})
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()["access_token"]

    def auth_headers(self, email: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.login(email)}"}

    def test_health_reports_durable_services(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertIn(body["status"], {"ok", "degraded"})
        self.assertEqual(body["services"]["sqlite"], "up")
        self.assertEqual(body["services"]["documents"], "up")
        self.assertEqual(response.headers["x-content-type-options"], "nosniff")
        self.assertEqual(response.headers["x-frame-options"], "DENY")

    def test_end_to_end_workflow_and_dashboard(self):
        farmer_headers = self.auth_headers("farmer@example.com")
        officer_headers = self.auth_headers("bihar.officer@example.com")
        inspector_headers = self.auth_headers("inspector@example.com")
        admin_headers = self.auth_headers("nmb.admin@example.com")

        profile_payload = {
            "name": "Demo Farmer",
            "mobile": "9876543210",
            "state_code": "BR",
            "district_code": "BR-PUR",
            "block_code": "BR-PUR-KR",
            "village_code": "BR-PUR-KR-001",
            "cultivation_type": "pond_based",
            "total_land_acres": 4.0,
            "makhana_area_acres": 2.0,
        }
        profile_res = self.client.put("/api/v1/beneficiary/profile", json=profile_payload, headers=farmer_headers)
        self.assertEqual(profile_res.status_code, 200, profile_res.text)

        aadhaar_res = self.client.post(
            "/api/v1/beneficiary/profile/verify-aadhaar",
            json={"aadhaar_number": "123412341234", "consent": True},
            headers=farmer_headers,
        )
        self.assertEqual(aadhaar_res.status_code, 200, aadhaar_res.text)
        self.assertEqual(aadhaar_res.json()["aadhaar_masked"], "XXXX-XXXX-1234")
        self.assertTrue(aadhaar_res.json()["identity_verified"])

        app_payload = {
            "scheme_component": "Makhana Cultivation Support",
            "pond_area_acres": 1.4,
            "requested_amount": 52000,
            "documents": [{"file_name": "bank-passbook.pdf", "document_type": "bank_proof"}],
            "geo_tag": {"latitude": 25.61, "longitude": 87.49, "accuracy": 12},
        }
        create_res = self.client.post("/api/v1/beneficiary/applications", json=app_payload, headers=farmer_headers)
        self.assertEqual(create_res.status_code, 200, create_res.text)
        application_id = create_res.json()["application_id"]

        clarification_res = self.client.post(
            f"/api/v1/officer/applications/{application_id}/clarifications",
            json={"query_text": "Please confirm bank proof."},
            headers=officer_headers,
        )
        self.assertEqual(clarification_res.status_code, 200, clarification_res.text)

        respond_res = self.client.post(
            f"/api/v1/beneficiary/applications/{application_id}/clarifications/respond",
            json={"response_text": "Updated document is attached in support records."},
            headers=farmer_headers,
        )
        self.assertEqual(respond_res.status_code, 200, respond_res.text)

        assign_res = self.client.post(
            f"/api/v1/officer/applications/{application_id}/inspection/assign",
            json={"inspector_email": "inspector@example.com"},
            headers=officer_headers,
        )
        self.assertEqual(assign_res.status_code, 200, assign_res.text)
        inspection_id = assign_res.json()["inspection_id"]

        complete_res = self.client.post(
            f"/api/v1/officer/inspections/{inspection_id}/complete",
            json={
                "remarks": "Verified on site.",
                "latitude": 25.62,
                "longitude": 87.48,
                "accuracy": 8,
                "photo_name": "inspection-proof.jpg",
            },
            headers=inspector_headers,
        )
        self.assertEqual(complete_res.status_code, 200, complete_res.text)

        recommend_res = self.client.post(
            f"/api/v1/officer/applications/{application_id}/recommend",
            json={"remarks": "Eligible after inspection."},
            headers=officer_headers,
        )
        self.assertEqual(recommend_res.status_code, 200, recommend_res.text)
        self.assertEqual(recommend_res.json()["current_status"], "Recommended by State")

        decision_res = self.client.post(
            f"/api/v1/nmb/applications/{application_id}/decision",
            json={"decision": "Approved", "remarks": "Approved for release."},
            headers=admin_headers,
        )
        self.assertEqual(decision_res.status_code, 200, decision_res.text)
        self.assertEqual(decision_res.json()["current_status"], "Approved")

        report_res = self.client.get("/api/v1/dashboard/summary", headers=admin_headers)
        self.assertEqual(report_res.status_code, 200, report_res.text)
        self.assertGreaterEqual(report_res.json()["kpis"]["applications"], 1)

        aap_res = self.client.post(
            "/api/v1/aap",
            json={
                "financial_year": "2027-28",
                "cultivation_target_hectares": 1500,
                "farmer_target": 6000,
                "infrastructure_target": 32,
                "budget_requested": 28000000,
                "remarks": "Expanded district coverage for next FY.",
            },
            headers=officer_headers,
        )
        self.assertEqual(aap_res.status_code, 200, aap_res.text)
        aap_id = aap_res.json()["aap_id"]

        aap_review_res = self.client.post(
            f"/api/v1/aap/{aap_id}/review",
            json={"decision": "Approved", "remarks": "Accepted for next planning cycle."},
            headers=admin_headers,
        )
        self.assertEqual(aap_review_res.status_code, 200, aap_review_res.text)
        self.assertEqual(aap_review_res.json()["current_status"], "Approved")

        budget_create_res = self.client.post(
            "/api/v1/budgets",
            json={
                "state_code": "BR",
                "component_name": "Training and Extension",
                "financial_year": "2026-27",
                "allocated_amount": 3500000,
                "released_amount": 1800000,
                "utilized_amount": 900000,
            },
            headers=admin_headers,
        )
        self.assertEqual(budget_create_res.status_code, 200, budget_create_res.text)
        budget_id = budget_create_res.json()["budget_id"]

        budget_update_res = self.client.post(
            f"/api/v1/budgets/{budget_id}/utilization",
            json={"released_amount": 2200000, "utilized_amount": 1250000, "remarks": "Q2 utilization update."},
            headers=officer_headers,
        )
        self.assertEqual(budget_update_res.status_code, 200, budget_update_res.text)
        self.assertEqual(budget_update_res.json()["utilized_amount"], 1250000)

        filtered_summary_res = self.client.get(
            "/api/v1/dashboard/summary?financial_year=2026-27&state_code=BR&quarter=Q1",
            headers=admin_headers,
        )
        self.assertEqual(filtered_summary_res.status_code, 200, filtered_summary_res.text)
        self.assertEqual(filtered_summary_res.json()["filters"]["financial_year"], "2026-27")

        csv_res = self.client.get(
            "/api/v1/reports/overview?format=csv&financial_year=2026-27&state_code=BR",
            headers=admin_headers,
        )
        self.assertEqual(csv_res.status_code, 200, csv_res.text)
        self.assertIn("metric,value", csv_res.text)

        notifications_res = self.client.get("/api/v1/notifications?limit=20", headers=admin_headers)
        self.assertEqual(notifications_res.status_code, 200, notifications_res.text)
        subjects = {entry["subject"] for entry in notifications_res.json()}
        self.assertIn("Application submitted", subjects)
        self.assertIn("AAP Approved", subjects)
        self.assertIn("Budget utilization updated", subjects)
        self.assertTrue(any("email" in entry["provider_results"] for entry in notifications_res.json()))

        system_res = self.client.get("/api/v1/system/overview", headers=admin_headers)
        self.assertEqual(system_res.status_code, 200, system_res.text)
        self.assertEqual(system_res.json()["services"]["sqlite"], "up")
        self.assertIn("notification_summary", system_res.json())
        self.assertIn("integrations", system_res.json())

        mock_notify_res = self.client.post(
            "/api/v1/integrations/mock/notify",
            json={
                "channel": "sms",
                "recipient": "9876543210",
                "template_key": "application_submitted",
                "message": "Demo notification for committee walkthrough.",
            },
            headers=admin_headers,
        )
        self.assertEqual(mock_notify_res.status_code, 200, mock_notify_res.text)
        self.assertEqual(mock_notify_res.json()["integration_type"], "notification")

        mock_kyc_res = self.client.post(
            "/api/v1/integrations/mock/aadhaar-kyc",
            json={"beneficiary_name": "Demo Farmer", "aadhaar_number": "123412341234", "consent": True},
            headers=admin_headers,
        )
        self.assertEqual(mock_kyc_res.status_code, 200, mock_kyc_res.text)
        self.assertEqual(mock_kyc_res.json()["provider_name"], "mock-aadhaar-vault")

        mock_dbt_res = self.client.post(
            "/api/v1/integrations/mock/dbt/disburse",
            json={
                "application_id": application_id,
                "beneficiary_name": "Demo Farmer",
                "bank_account_last4": "4321",
                "amount": 45000,
            },
            headers=admin_headers,
        )
        self.assertEqual(mock_dbt_res.status_code, 200, mock_dbt_res.text)
        self.assertEqual(mock_dbt_res.json()["integration_type"], "payments")

        integration_logs_res = self.client.get("/api/v1/integrations/mock/logs?limit=10", headers=admin_headers)
        self.assertEqual(integration_logs_res.status_code, 200, integration_logs_res.text)
        integration_types = {entry["integration_type"] for entry in integration_logs_res.json()}
        self.assertIn("notification", integration_types)
        self.assertIn("identity", integration_types)
        self.assertIn("payments", integration_types)

        batch_res = self.client.post(
            "/api/v1/nmb/applications/batch-decision",
            json={"application_ids": [application_id], "decision": "Returned", "remarks": "Batch reviewed."},
            headers=admin_headers,
        )
        self.assertEqual(batch_res.status_code, 200, batch_res.text)
        self.assertEqual(batch_res.json()["processed"][0]["status"], "Returned")

        audit_res = self.client.get("/api/v1/audit/logs", headers=admin_headers)
        self.assertEqual(audit_res.status_code, 200, audit_res.text)
        modules = {entry["module"] for entry in audit_res.json()}
        self.assertIn("application", modules)
        self.assertIn("aap", modules)
        self.assertIn("budget", modules)

    def test_invalid_document_type_rejected(self):
        farmer_headers = self.auth_headers("farmer@example.com")
        payload = {
            "scheme_component": "Makhana Cultivation Support",
            "pond_area_acres": 1.0,
            "requested_amount": 10000,
            "documents": [{"file_name": "payload.exe", "document_type": "identity_proof"}],
            "geo_tag": {"latitude": 25.61, "longitude": 87.49, "accuracy": 12},
        }
        response = self.client.post("/api/v1/beneficiary/applications", json=payload, headers=farmer_headers)
        self.assertEqual(response.status_code, 400, response.text)
        self.assertIn("Unsupported file type", response.text)

    def test_aadhaar_verification_requires_consent(self):
        farmer_headers = self.auth_headers("farmer@example.com")
        self.client.put(
            "/api/v1/beneficiary/profile",
            json={
                "name": "Demo Farmer",
                "mobile": "9876543210",
                "state_code": "BR",
                "district_code": "BR-PUR",
                "block_code": "BR-PUR-KR",
                "village_code": "BR-PUR-KR-001",
                "cultivation_type": "pond_based",
                "total_land_acres": 4.0,
                "makhana_area_acres": 2.0,
            },
            headers=farmer_headers,
        )
        response = self.client.post(
            "/api/v1/beneficiary/profile/verify-aadhaar",
            json={"aadhaar_number": "123412341234", "consent": False},
            headers=farmer_headers,
        )
        self.assertEqual(response.status_code, 400, response.text)
        self.assertIn("Consent is required", response.text)

    def test_sms_notification_requires_mobile_number(self):
        admin_headers = self.auth_headers("nmb.admin@example.com")
        response = self.client.post(
            "/api/v1/integrations/mock/notify",
            json={
                "channel": "sms",
                "recipient": "farmer@example.com",
                "template_key": "application_submitted",
                "message": "Invalid recipient check.",
            },
            headers=admin_headers,
        )
        self.assertEqual(response.status_code, 400, response.text)
        self.assertIn("10 digit mobile number", response.text)


if __name__ == "__main__":
    unittest.main()
