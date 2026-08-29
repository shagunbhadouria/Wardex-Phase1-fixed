"""Tests for incident routes (Rule R-44, R-17)."""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_incidents_returns_empty_list_stub() -> None:
    response = client.get("/api/v1/incidents")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["incidents"] == []
    assert body["data"]["total"] == 0


def test_list_incidents_accepts_optional_filters() -> None:
    response = client.get(
        "/api/v1/incidents",
        params={"status_filter": "open", "severity": "high", "limit": 5},
    )
    assert response.status_code == 200


def test_get_incident_returns_stub_detail() -> None:
    incident_id = uuid4()
    response = client.get(f"/api/v1/incidents/{incident_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["incident"] is None
    assert body["data"]["remediations"] == []
    assert body["data"]["llm_calls"] == []
    assert body["data"]["similar_past"] == []


def test_get_incident_rejects_invalid_uuid() -> None:
    response = client.get("/api/v1/incidents/not-a-uuid")
    assert response.status_code == 422


def test_resolve_incident_returns_stub_response() -> None:
    incident_id = uuid4()
    response = client.post(
        f"/api/v1/incidents/{incident_id}/resolve", json={"notes": "fixed via restart"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["incident"] is None
    assert body["data"]["postmortem"] is None


def test_resolve_incident_accepts_no_notes() -> None:
    incident_id = uuid4()
    response = client.post(f"/api/v1/incidents/{incident_id}/resolve", json={})
    assert response.status_code == 200
