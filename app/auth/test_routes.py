"""Tests for auth routes (Rule R-44, R-17)."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_google_auth_returns_stub_tokens() -> None:
    """Phase 2 stub: no real OAuth exchange yet, but the contract shape holds."""
    response = client.post("/api/v1/auth/google", json={"code": "any-code"})
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["token"] == "stub-not-issued"
    assert body["data"]["refresh_token"] == "stub-not-issued"
    assert body["data"]["user"] is None
    assert body["error"] is None


def test_google_auth_rejects_missing_code() -> None:
    """Boundary validation (R-31): missing required field is a 422, not a 500."""
    response = client.post("/api/v1/auth/google", json={})
    assert response.status_code == 422


def test_refresh_token_returns_stub_tokens() -> None:
    response = client.post(
        "/api/v1/auth/refresh", json={"refresh_token": "any-refresh-token"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["token"] == "stub-not-issued"


def test_refresh_token_rejects_missing_field() -> None:
    response = client.post("/api/v1/auth/refresh", json={})
    assert response.status_code == 422
