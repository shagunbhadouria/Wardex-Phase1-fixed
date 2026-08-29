"""Tests for deployment routes (Rule R-44, R-17)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_deployment_webhook_acknowledges_with_zero_risk_stub() -> None:
    """Phase 2 stub: no HMAC verification (R-54) or XGBoost scoring yet
    (both Phase 6) — this only proves the endpoint accepts and acks."""
    response = client.post(
        "/api/v1/deployments/webhook",
        json={"commit_sha": "abc123", "author": "octocat"},
    )
    assert response.status_code == 202
    body = response.json()
    assert body["success"] is True
    assert body["data"]["risk_score"] == 0.0
    assert body["data"]["risk_explanation"] is None
    assert "deployment_id" in body["data"]


def test_deployment_webhook_accepts_empty_body() -> None:
    """The stub deliberately accepts any payload shape (Phase 6 will lock
    this down against the real GitHub webhook schema + HMAC)."""
    response = client.post("/api/v1/deployments/webhook")
    assert response.status_code == 202


def test_list_deployments_returns_empty_list_stub() -> None:
    response = client.get("/api/v1/deployments")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["deployments"] == []


def test_list_deployments_accepts_optional_filters() -> None:
    response = client.get(
        "/api/v1/deployments",
        params={
            "service_id": "00000000-0000-0000-0000-000000000000",
            "limit": 10,
        },
    )
    assert response.status_code == 200


def test_list_deployments_rejects_invalid_service_id() -> None:
    response = client.get(
        "/api/v1/deployments", params={"service_id": "not-a-uuid"}
    )
    assert response.status_code == 422
