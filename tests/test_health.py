from unittest.mock import patch

from app import app


def test_health_check_healthy():
    app.config["TESTING"] = True

    with patch("certificados.views.ping_db", return_value=(True, "connected")):
        client = app.test_client()
        response = client.get("/health")

        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert data["database"]["connected"] is True
        assert data["database"]["message"] == "connected"


def test_health_check_unhealthy():
    app.config["TESTING"] = True

    with patch("certificados.views.ping_db", return_value=(False, "Connection timeout")):
        client = app.test_client()
        response = client.get("/health")

        assert response.status_code == 503
        data = response.get_json()
        assert data["status"] == "unhealthy"
        assert data["database"]["connected"] is False
        assert data["database"]["message"] == "Connection timeout"
