"""Chaos engineering routes (Blueprint v2 Section 2.4).

Phase 2 stub: accepts the locked request/response shape, returns the
standard envelope. Actual scenario injection and RBAC enforcement are
wired up in later phases — see R-69/R-77.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, status

from app.chaos.schemas import ChaosInjectRequest, ChaosInjectResponse
from app.shared.types import ApiResponse

router = APIRouter(prefix="/chaos", tags=["Chaos"])


@router.post(
    "/inject",
    response_model=ApiResponse[ChaosInjectResponse],
    status_code=status.HTTP_200_OK,
    summary="Inject a chaos engineering scenario (admin only)",
)
async def inject_chaos(payload: ChaosInjectRequest) -> ApiResponse[ChaosInjectResponse]:
    """Phase 2 stub.

    TECH DEBT: SEC-002 — this endpoint has no auth/RBAC enforcement yet.
    v2 Section 2.4 requires JWT + Admin role on this route (it can start
    real infrastructure faults). Auth middleware doesn't exist until
    Phase 4. Do not deploy this stub anywhere reachable outside a local
    dev environment until Phase 4 auth is wired in front of it.
    """
    return ApiResponse[ChaosInjectResponse](
        success=True,
        data=ChaosInjectResponse(started_at=datetime.now(timezone.utc)),
    )
