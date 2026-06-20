import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


class ChatbotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def login(self, email: str, password: str = "Pass@123") -> str:
        response = self.client.post("/api/v1/auth/login", json={"email": email, "password": password})
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()["access_token"]

    def test_public_chat_returns_grounded_answer(self):
        response = self.client.post(
            "/api/v1/chat/message",
            json={"message": "What does clarification raised mean?", "page": "helpdesk", "language": "en"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertIn("answer", body)
        self.assertGreater(len(body["sources"]), 0)
        self.assertIn(body["mode"], {"retrieval_fallback", "azure_grounded"})
        self.assertNotIn("Based on the approved", body["answer"])
        self.assertNotIn("Question:", body["answer"])

    def test_public_chat_returns_helpful_fallback_for_unknown_query(self):
        response = self.client.post(
            "/api/v1/chat/message",
            json={"message": "Tell me about marine export tax waivers", "page": "home", "language": "en"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertIn("helpdesk", body["answer"].lower())
        self.assertTrue(body["fallback_used"])

    def test_streaming_endpoint_returns_delta_and_complete_events(self):
        response = self.client.post(
            "/api/v1/chat/stream",
            json={"message": "What is this portal used for?", "page": "home", "language": "en"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertIn('"type": "delta"', response.text)
        self.assertIn('"type": "complete"', response.text)

    def test_beneficiary_chat_uses_runtime_context(self):
        token = self.login("farmer@example.com")
        response = self.client.post(
            "/api/v1/chat/message",
            headers={"Authorization": f"Bearer {token}"},
            json={"message": "What is my current application status?", "page": "beneficiary", "language": "en"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertIn(body["mode"], {"beneficiary_runtime_fallback", "azure_grounded"})
        self.assertTrue(any(source["category"] == "runtime" for source in body["sources"]))

    def test_admin_chat_uses_operations_context(self):
        token = self.login("nmb.admin@example.com")
        response = self.client.post(
            "/api/v1/chat/message",
            headers={"Authorization": f"Bearer {token}"},
            json={"message": "Summarize the AAP and budget situation.", "page": "dashboard", "language": "en"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertIn(body["mode"], {"operations_runtime_fallback", "azure_grounded"})
        self.assertTrue(any(source["category"] == "runtime" for source in body["sources"]))

    def test_chat_history_and_analytics_endpoints(self):
        farmer_token = self.login("farmer@example.com")
        admin_token = self.login("nmb.admin@example.com")
        self.client.post(
            "/api/v1/chat/message",
            headers={"Authorization": f"Bearer {farmer_token}"},
            json={"message": "Do I have any open clarification?", "page": "beneficiary", "language": "en"},
        )
        history_res = self.client.get("/api/v1/chat/history?limit=5", headers={"Authorization": f"Bearer {farmer_token}"})
        self.assertEqual(history_res.status_code, 200, history_res.text)
        self.assertGreaterEqual(len(history_res.json()), 1)

        analytics_res = self.client.get("/api/v1/chat/analytics", headers={"Authorization": f"Bearer {admin_token}"})
        self.assertEqual(analytics_res.status_code, 200, analytics_res.text)
        self.assertIn("total_chats", analytics_res.json())
