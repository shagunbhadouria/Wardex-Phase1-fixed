"""Pydantic schemas for deployment routes (Blueprint v2 Section 2.4)."""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class DeploymentWebhookResponse(BaseModel):
    """Response payload for POST /deployments/webhook."""

    deployment_id: UUID
    risk_score: float
    risk_explanation: Optional[dict[str, Any]] = None


class DeploymentResponse(BaseModel):
    """A single deployment record."""

    id: UUID
    service_id: UUID
    commit_sha: str
    author_github: str
    risk_score: Optional[float] = None
    outcome: Optional[str] = None
    deployed_at: datetime


class DeploymentListResponse(BaseModel):
    """Response payload for GET /deployments."""

    deployments: list[DeploymentResponse]
