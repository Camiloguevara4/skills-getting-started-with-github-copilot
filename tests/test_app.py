def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball",
        "Art Studio",
        "Music Band",
        "Debate Club",
        "Science Club",
    }

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert set(payload.keys()) == expected_activity_names
    assert all("participants" in details for details in payload.values())


def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in participants


def test_signup_returns_404_for_missing_activity(client):
    # Arrange
    activity_name = "Robotics Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_remove_participant_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/remove/{email}")
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in participants


def test_remove_returns_404_for_missing_activity(client):
    # Arrange
    activity_name = "Robotics Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/remove/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_remove_returns_400_for_unregistered_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "unregistered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/remove/{email}")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student not registered for this activity"}