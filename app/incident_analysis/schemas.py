"""Pydantic schemas for incident routes (Blueprint v2 Section 2.4)."""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class IncidentSummary(BaseModel):
    """A single incident record in list views."""

    id: UUID
    service_id: UUID
    status: str
    severity: str
    detected_at: datetime
    resolved_at: Optional[datetime] = None


class IncidentListResponse(BaseModel):
    """Response payload for GET /incidents."""

    incidents: list[IncidentSummary]
    total: int


class IncidentDetail(BaseModel):
    """Full incident detail, matches GET /incidents/:id."""

    incident: Optional[IncidentSummary] = None
    remediations: list[dict[str, Any]] = []
    llm_calls: list[dict[str, Any]] = []
    similar_past: list[dict[str, Any]] = []


class IncidentResolveRequest(BaseModel):
    """Request body for POST /incidents/:id/resolve."""

    notes: Optional[str] = None


class IncidentResolveResponse(BaseModel):
    """Response payload for POST /incidents/:id/resolve."""

    incident: Optional[IncidentSummary] = None
    postmortem: Optional[str] = None
