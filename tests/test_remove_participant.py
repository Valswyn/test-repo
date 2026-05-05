"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""
import pytest


class TestRemoveParticipant:
    """Test cases for removing participants from activities"""

    def test_successful_removal(self, client):
        """Test successful removal of a participant"""
        # Arrange
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Verify participant exists initially
        initial_response = client.get("/activities")
        initial_data = initial_response.json()
        assert email in initial_data[activity]["participants"]

        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Removed {email} from {activity}" in data["message"]

        # Verify participant was removed
        final_response = client.get("/activities")
        final_data = final_response.json()
        assert email not in final_data[activity]["participants"]

    def test_remove_nonexistent_activity(self, client):
        """Test removal from non-existent activity returns 404"""
        # Arrange
        email = "test@mergington.edu"
        invalid_activity = "NonExistent Club"

        # Act
        response = client.delete(f"/activities/{invalid_activity}/participants/{email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_remove_nonexistent_participant(self, client):
        """Test removal of non-existent participant returns 404"""
        # Arrange
        email = "nonexistent@mergington.edu"
        activity = "Chess Club"

        # Act
        response = client.delete(f"/activities/{activity}/participants/{email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Participant not found" in data["detail"]

    def test_remove_preserves_other_participants(self, client):
        """Test that removing one participant doesn't affect others"""
        # Arrange
        activity = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"

        # Verify both exist
        initial_response = client.get("/activities")
        initial_data = initial_response.json()
        assert email_to_remove in initial_data[activity]["participants"]
        assert email_to_keep in initial_data[activity]["participants"]

        # Act - Remove one participant
        response = client.delete(f"/activities/{activity}/participants/{email_to_remove}")
        assert response.status_code == 200

        # Assert - Other participant still there
        final_response = client.get("/activities")
        final_data = final_response.json()
        assert email_to_remove not in final_data[activity]["participants"]
        assert email_to_keep in final_data[activity]["participants"]

    def test_remove_preserves_other_activities(self, client):
        """Test that removing from one activity doesn't affect others"""
        # Arrange
        activity_to_modify = "Chess Club"
        activity_to_check = "Programming Class"
        email = "michael@mergington.edu"

        # Get initial counts
        initial_response = client.get("/activities")
        initial_data = initial_response.json()
        initial_count = len(initial_data[activity_to_check]["participants"])

        # Act - Remove from Chess Club
        response = client.delete(f"/activities/{activity_to_modify}/participants/{email}")
        assert response.status_code == 200

        # Assert - Programming Class unchanged
        final_response = client.get("/activities")
        final_data = final_response.json()
        final_count = len(final_data[activity_to_check]["participants"])
        assert final_count == initial_count

    @pytest.mark.parametrize("activity_name,email", [
        ("Chess Club", "michael@mergington.edu"),
        ("Programming Class", "emma@mergington.edu"),
        ("Gym Class", "john@mergington.edu"),
        ("Art Studio", "grace@mergington.edu"),
        ("Music Band", "lucas@mergington.edu"),
        ("Debate Team", "noah@mergington.edu"),
        ("Science Club", "ava@mergington.edu")
    ])
    def test_remove_works_for_all_initial_participants(self, client, activity_name, email):
        """Test removal works for all initially enrolled participants"""
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

        # Verify removal
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity_name]["participants"]