"""Tests for GET / root endpoint"""
import pytest


class TestRootRedirect:
    """Test cases for root endpoint redirect"""

    def test_root_redirects_to_index_html(self, client):
        """Test that GET / redirects to /static/index.html"""
        # Act
        response = client.get("/", follow_redirects=False)  # Don't follow redirect

        # Assert
        assert response.status_code == 307  # Temporary redirect
        assert response.headers["location"] == "/static/index.html"

    def test_root_redirect_followed(self, client):
        """Test that following the redirect reaches the static file"""
        # Act
        response = client.get("/", follow_redirects=True)  # Follow redirect

        # Assert
        assert response.status_code == 200
        # Note: In test environment, static files might not be served the same way
        # This test mainly verifies the redirect logic