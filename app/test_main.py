"""Health check and API response envelope tests."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_endpoint() -> None:
    """Verifies GET /health returns 200 with standard response envelope."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "starting"
    assert "version" in data["meta"]
    assert "request_id" in data["meta"]
    assert data["error"] is None


def test_health_check_request_id_header() -> None:
    """Verifies X-Request-ID and X-Process-Time headers are injected by middleware."""
    response = client.get("/health")
    assert "x-request-id" in response.headers
    assert "x-process-time" in response.headers
