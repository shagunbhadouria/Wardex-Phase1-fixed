"""Pydantic schemas for the chaos injection route (Blueprint v2 Section 2.4)."""

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ChaosInjectRequest(BaseModel):
    """Request body for POST /chaos/inject."""

    scenario: str
    service_id: UUID
    duration_seconds: int = 60


class ChaosInjectResponse(BaseModel):
    """Response payload for POST /chaos/inject."""

    scenario_id: UUID = Field(default_factory=uuid4)
    started_at: datetime
