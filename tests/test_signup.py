"""Tests for POST /activities/{activity_name}/signup endpoint"""
import pytest


class TestSignup:
    """Test cases for student signup functionality"""

    def test_successful_signup(self, client):
        """Test successful signup for an activity"""
        # Arrange
        email = "test@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Signed up {email} for {activity}" in data["message"]

        # Verify participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity]["participants"]

    def test_signup_invalid_activity(self, client):
        """Test signup for non-existent activity returns 404"""
        # Arrange
        email = "test@mergington.edu"
        invalid_activity = "NonExistent Club"

        # Act
        response = client.post(f"/activities/{invalid_activity}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_already_registered(self, client):
        """Test signup when student is already registered returns 400"""
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Student already signed up" in data["detail"]

    def test_signup_activity_at_capacity(self, client):
        """Test signup when activity is at max capacity returns 400"""
        # Arrange - Fill up Debate Team (max 16, currently 1 participant)
        activity = "Debate Team"
        for i in range(15):  # Add 15 more to reach capacity
            email = f"student{i}@mergington.edu"
            response = client.post(f"/activities/{activity}/signup?email={email}")
            assert response.status_code == 200

        # Now try to add one more (should fail)
        final_email = "final@mergington.edu"
        response = client.post(f"/activities/{activity}/signup?email={final_email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Activity is full" in data["detail"]

    def test_signup_preserves_other_activities(self, client):
        """Test that signup doesn't affect other activities"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity = "Programming Class"

        # Get initial state
        initial_response = client.get("/activities")
        initial_data = initial_response.json()
        initial_chess_count = len(initial_data["Chess Club"]["participants"])

        # Act - Signup for Programming Class
        response = client.post(f"/activities/{activity}/signup?email={email}")
        assert response.status_code == 200

        # Assert - Chess Club unchanged
        final_response = client.get("/activities")
        final_data = final_response.json()
        final_chess_count = len(final_data["Chess Club"]["participants"])
        assert final_chess_count == initial_chess_count

    @pytest.mark.parametrize("activity_name", [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Art Studio",
        "Music Band",
        "Debate Team",
        "Science Club"
    ])
    def test_signup_works_for_all_activities(self, client, activity_name):
        """Test signup works for all existing activities"""
        # Arrange
        email = f"test_{activity_name.replace(' ', '_')}@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]