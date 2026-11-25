import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app import activities, app


class UnregisterActivityTests(unittest.TestCase):
    def setUp(self):
        self.activity = {
            "description": "Test",
            "schedule": "Friday",
            "max_participants": 3,
            "participants": ["student@example.com", "other@example.com", "student@example.com"],
        }
        self.patcher = patch.dict(activities, {"Test Activity": self.activity})
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.client = TestClient(app)
        self.addCleanup(self.client.close)

    def test_unregister_removes_all_registrations_for_student(self):
        response = self.client.delete(
            "/activities/Test%20Activity/signup",
            params={"email": "student@example.com"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.activity["participants"], ["other@example.com"])
        self.assertEqual(
            self.client.get("/activities").json()["Test Activity"]["participants"],
            ["other@example.com"],
        )

    def test_unknown_activity_returns_not_found(self):
        response = self.client.delete(
            "/activities/Unknown/signup", params={"email": "student@example.com"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Activity not found")

    def test_unknown_participant_returns_not_found_without_changes(self):
        response = self.client.delete(
            "/activities/Test%20Activity/signup", params={"email": "missing@example.com"}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Student not signed up for this activity")
        self.assertEqual(
            self.activity["participants"],
            ["student@example.com", "other@example.com", "student@example.com"],
        )


if __name__ == "__main__":
    unittest.main()
