"""Tests for the chaos injection route (Rule R-44, R-17).

TECH DEBT: SEC-002 — these tests do NOT verify auth/RBAC enforcement,
because none exists yet (Phase 4). Once JWT + Admin role gating lands
in front of this route, add a 401/403 test here for unauthenticated
and non-admin callers — that is the actual security-relevant behavior
this stub cannot be tested for yet.
"""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_inject_chaos_returns_stub_response() -> None:
    response = client.post(
        "/api/v1/chaos/inject",
        json={
            "scenario": "high-error-rate",
            "service_id": str(uuid4()),
            "duration_seconds": 120,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "scenario_id" in body["data"]
    assert "started_at" in body["data"]


def test_inject_chaos_defaults_duration() -> None:
    response = client.post(
        "/api/v1/chaos/inject",
        json={"scenario": "memory-leak", "service_id": str(uuid4())},
    )
    assert response.status_code == 200


def test_inject_chaos_rejects_missing_scenario() -> None:
    response = client.post(
        "/api/v1/chaos/inject", json={"service_id": str(uuid4())}
    )
    assert response.status_code == 422


def test_inject_chaos_rejects_invalid_service_id() -> None:
    response = client.post(
        "/api/v1/chaos/inject", json={"scenario": "x", "service_id": "not-a-uuid"}
    )
    assert response.status_code == 422
