"""Tests for service and metric routes (Rule R-44, R-17)."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_services_returns_empty_list_stub() -> None:
    """Phase 2 stub: no DB reads yet (Phase 3), so this is always empty."""
    response = client.get("/api/v1/services")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["services"] == []


def test_create_service_echoes_input_with_generated_fields() -> None:
    response = client.post(
        "/api/v1/services", json={"name": "payment-service", "environment": "staging"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "payment-service"
    assert body["data"]["environment"] == "staging"
    assert body["data"]["baseline_cpu"] == 0.0
    assert "id" in body["data"]
    assert "created_at" in body["data"]


def test_create_service_defaults_environment_to_production() -> None:
    response = client.post("/api/v1/services", json={"name": "auth-service"})
    assert response.status_code == 201
    assert response.json()["data"]["environment"] == "production"


def test_create_service_rejects_missing_name() -> None:
    response = client.post("/api/v1/services", json={"environment": "production"})
    assert response.status_code == 422


def test_get_service_metrics_returns_empty_list_stub() -> None:
    service_id = uuid4()
    response = client.get(f"/api/v1/services/{service_id}/metrics")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["metrics"] == []


def test_get_service_metrics_rejects_invalid_uuid() -> None:
    response = client.get("/api/v1/services/not-a-uuid/metrics")
    assert response.status_code == 422


def test_ingest_service_metrics_acknowledges_receipt() -> None:
    service_id = uuid4()
    response = client.post(
        f"/api/v1/services/{service_id}/metrics",
        json={
            "cpu_percent": 42.5,
            "memory_percent": 60.0,
            "error_rate": 0.01,
            "api_latency_ms": 120.0,
            "request_count": 500,
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "received"
    assert body["data"]["anomaly_detected"] is False
    assert body["data"]["snapshot_id"] is None
    assert body["data"]["service_id"] == str(service_id)


def test_ingest_service_metrics_rejects_missing_required_field() -> None:
    service_id = uuid4()
    response = client.post(
        f"/api/v1/services/{service_id}/metrics",
        json={"cpu_percent": 10.0},  # missing memory_percent, error_rate, etc.
    )
    assert response.status_code == 422
