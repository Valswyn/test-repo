"""Tests for GET /activities endpoint"""
import pytest


class TestGetActivities:
    """Test cases for retrieving all activities"""

    def test_get_all_activities_success(self, client):
        """Test successful retrieval of all activities"""
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 7  # Should have 7 activities

        # Check structure of first activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_activities_contain_expected_data(self, client):
        """Test that activities contain the expected data"""
        response = client.get("/activities")
        data = response.json()

        # Check Chess Club data
        chess = data["Chess Club"]
        assert chess["description"] == "Learn strategies and compete in chess tournaments"
        assert chess["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
        assert chess["max_participants"] == 12
        assert "michael@mergington.edu" in chess["participants"]
        assert "daniel@mergington.edu" in chess["participants"]

    def test_all_activities_have_required_fields(self, client):
        """Test that all activities have required fields"""
        response = client.get("/activities")
        data = response.json()

        required_fields = ["description", "schedule", "max_participants", "participants"]

        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data, f"Activity {activity_name} missing {field}"
                if field == "participants":
                    assert isinstance(activity_data[field], list)
                elif field == "max_participants":
                    assert isinstance(activity_data[field], int)
                    assert activity_data[field] > 0
                else:
                    assert isinstance(activity_data[field], str)
                    assert len(activity_data[field]) > 0