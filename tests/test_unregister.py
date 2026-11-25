def test_unregister_removes_all_registrations_for_student(activity_client):
    client, activity = activity_client

    response = client.delete(
        "/activities/Test%20Activity/signup",
        params={"email": "student@example.com"},
    )
    activities_response = client.get("/activities")

    assert response.status_code == 200
    assert activity["participants"] == ["other@example.com"]
    assert activities_response.json()["Test Activity"]["participants"] == ["other@example.com"]


def test_unknown_activity_returns_not_found(activity_client):
    client, _ = activity_client

    response = client.delete(
        "/activities/Unknown/signup", params={"email": "student@example.com"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unknown_participant_returns_not_found_without_changes(activity_client):
    client, activity = activity_client

    response = client.delete(
        "/activities/Test%20Activity/signup", params={"email": "missing@example.com"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"
    assert activity["participants"] == [
        "student@example.com",
        "other@example.com",
        "student@example.com",
    ]
