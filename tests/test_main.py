"""
Unit tests for FastAPI app definition in main.py
"""
import unittest
from fastapi.testclient import TestClient
from app.main import app


class TestMainApp(unittest.TestCase):
    def test_app_instance_created(self):
        self.assertEqual(app.title, "FastAPI")
        self.assertTrue(hasattr(app, "router"))
        self.assertTrue(callable(app.router.include_router))

    def test_app_responds_to_request(self):
        client = TestClient(app)
        response = client.post("/moderate", json={
            "input": "Test ethical query",
            "environment": "lab",
            "user_role": "guest"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["response"].startswith(
            "[APPROVED") or response.json()["response"].startswith("[BLOCKED"))


if __name__ == '__main__':
    unittest.main()
