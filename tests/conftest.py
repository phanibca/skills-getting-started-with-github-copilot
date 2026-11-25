from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def activity_client():
    activity = {
        "description": "Test",
        "schedule": "Friday",
        "max_participants": 10,
        "participants": ["student@example.com", "other@example.com", "student@example.com"],
    }
    with patch.dict(activities, {"Test Activity": activity}, clear=True), TestClient(app) as client:
        yield client, activity
