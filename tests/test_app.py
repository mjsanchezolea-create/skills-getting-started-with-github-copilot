from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_signup_adds_participant_to_activity():
    activity_name = "Chess Club"
    email = f"{uuid4().hex}@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    updated_activity = client.get("/activities").json()[activity_name]
    assert email in updated_activity["participants"]

    client.post(f"/activities/{activity_name}/unregister?email={email}")


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    initial_activity = client.get("/activities").json()[activity_name]
    assert email in initial_activity["participants"]

    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    updated_activity = client.get("/activities").json()[activity_name]
    assert email not in updated_activity["participants"]
