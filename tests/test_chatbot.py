import unittest
import json
from unittest.mock import MagicMock, patch
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.chatbot import ContextSource, _gemini_chat_attempt
from backend.app.core import config as config_module
from backend.app.core.config import settings


class ChatbotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        self._chatbot_enabled = settings.chatbot_enabled
        self._gemini_api_key = settings.gemini_api_key
        settings.chatbot_enabled = False
        settings.gemini_api_key = ""

    def tearDown(self):
        settings.chatbot_enabled = self._chatbot_enabled
        settings.gemini_api_key = self._gemini_api_key

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
        self.assertIn(body["mode"], {"retrieval_fallback", "gemini_grounded"})
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

    def test_chat_diagnostics_exposes_mode_and_ranked_sources(self):
        response = self.client.post(
            "/api/v1/chat/diagnostics",
            json={"message": "Which users are supported here?", "page": "home", "language": "en"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertIn("gemini_ready", body)
        self.assertIn("gemini_configured", body)
        self.assertIn("provider_error", body)
        self.assertIn("fallback_used", body)
        self.assertIn("top_sources", body)
        self.assertGreater(len(body["top_sources"]), 0)
        self.assertIn("score", body["top_sources"][0])

    def test_beneficiary_chat_uses_runtime_context(self):
        token = self.login("farmer@example.com")
        response = self.client.post(
            "/api/v1/chat/message",
            headers={"Authorization": f"Bearer {token}"},
            json={"message": "What is my current application status?", "page": "beneficiary", "language": "en"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertIn(body["mode"], {"beneficiary_runtime_fallback", "gemini_grounded"})
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
        self.assertIn(body["mode"], {"operations_runtime_fallback", "gemini_grounded"})
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

    def test_gemini_request_uses_grounded_context_and_parses_response(self):
        settings.chatbot_enabled = True
        settings.gemini_api_key = "test-key"
        source = ContextSource(
            source_id="official/test",
            title="Approved guidance",
            category="official",
            summary="Approved summary",
            text="Only this approved fact may be used.",
        )
        response = MagicMock()
        response.read.return_value = json.dumps(
            {"candidates": [{"content": {"parts": [{"text": "Grounded Gemini answer"}]}}]}
        ).encode("utf-8")
        urlopen = MagicMock()
        urlopen.return_value.__enter__.return_value = response

        with patch("backend.app.chatbot.request.urlopen", urlopen):
            answer, provider_error = _gemini_chat_attempt("What is approved?", "home", "en", None, [source])

        self.assertEqual(answer, "Grounded Gemini answer")
        self.assertIsNone(provider_error)
        sent_request = urlopen.call_args.args[0]
        self.assertIn("gemini-3.5-flash:generateContent", sent_request.full_url)
        self.assertEqual(sent_request.get_header("X-goog-api-key"), "test-key")
        sent_body = json.loads(sent_request.data.decode("utf-8"))
        self.assertIn("Only this approved fact may be used.", sent_body["contents"][0]["parts"][0]["text"])

    def test_vercel_default_data_dir_uses_tmp_storage(self):
        with patch.dict("os.environ", {"VERCEL": "1"}, clear=False):
            self.assertEqual(config_module._default_data_dir(), Path("/tmp/national-makhana-portal"))
