def test_list_activities_returns_activity_details(activity_client):
    client, activity = activity_client

    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == {"Test Activity": activity}


def test_signup_adds_participant(activity_client):
    client, activity = activity_client
    email = "new@example.com"
    participants_before = activity["participants"].copy()

    response = client.post("/activities/Test%20Activity/signup", params={"email": email})
    activities_response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Test Activity"}
    assert activity["participants"] == participants_before + [email]
    assert activities_response.json()["Test Activity"]["participants"] == activity["participants"]


def test_duplicate_signup_is_rejected(activity_client):
    client, activity = activity_client
    participants_before = activity["participants"].copy()

    response = client.post(
        "/activities/Test%20Activity/signup", params={"email": "student@example.com"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    assert activity["participants"] == participants_before


def test_signup_for_unknown_activity_is_rejected(activity_client):
    client, activity = activity_client
    participants_before = activity["participants"].copy()

    response = client.post("/activities/Unknown/signup", params={"email": "new@example.com"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
    assert activity["participants"] == participants_before


def test_signup_requires_email(activity_client):
    client, activity = activity_client
    participants_before = activity["participants"].copy()

    response = client.post("/activities/Test%20Activity/signup")

    assert response.status_code == 422
    assert activity["participants"] == participants_before


def test_participant_can_register_again_after_unregistering(activity_client):
    client, activity = activity_client
    email = "new@example.com"
    url = "/activities/Test%20Activity/signup"

    signup = client.post(url, params={"email": email})
    assert signup.status_code == 200
    assert email in activity["participants"]

    unregister = client.delete(url, params={"email": email})
    assert unregister.status_code == 200
    assert email not in activity["participants"]

    signup_again = client.post(url, params={"email": email})
    assert signup_again.status_code == 200
    assert activity["participants"].count(email) == 1
