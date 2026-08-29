"""Incident routes (Blueprint v2 Section 2.4).

Phase 2 stubs: accept the locked request/response shape, return the
standard envelope. LangGraph analysis (Phase 7), Correlation Guard,
and postmortem generation are wired up in later phases — see R-69/R-77.
"""

from uuid import UUID

from fastapi import APIRouter

from app.incident_analysis.schemas import (
    IncidentDetail,
    IncidentListResponse,
    IncidentResolveRequest,
    IncidentResolveResponse,
)
from app.shared.types import ApiResponse

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.get(
    "",
    response_model=ApiResponse[IncidentListResponse],
    summary="List incidents, optionally filtered by status/severity",
)
async def list_incidents(
    status_filter: str | None = None,
    severity: str | None = None,
    limit: int = 50,
) -> ApiResponse[IncidentListResponse]:
    """Phase 2 stub — reads from PostgreSQL are wired up in Phase 3."""
    return ApiResponse[IncidentListResponse](
        success=True,
        data=IncidentListResponse(incidents=[], total=0),
    )


@router.get(
    "/{incident_id}",
    response_model=ApiResponse[IncidentDetail],
    summary="Get full incident detail",
)
async def get_incident(incident_id: UUID) -> ApiResponse[IncidentDetail]:
    """Phase 2 stub — reads from PostgreSQL are wired up in Phase 3."""
    return ApiResponse[IncidentDetail](
        success=True,
        data=IncidentDetail(),
    )


@router.post(
    "/{incident_id}/resolve",
    response_model=ApiResponse[IncidentResolveResponse],
    summary="Mark an incident resolved and generate a postmortem",
)
async def resolve_incident(
    incident_id: UUID,
    payload: IncidentResolveRequest,
) -> ApiResponse[IncidentResolveResponse]:
    """Phase 2 stub — postmortem generation (one Groq call) is wired up
    once the LLM pipeline exists in Phase 7."""
    return ApiResponse[IncidentResolveResponse](
        success=True,
        data=IncidentResolveResponse(incident=None, postmortem=None),
    )
