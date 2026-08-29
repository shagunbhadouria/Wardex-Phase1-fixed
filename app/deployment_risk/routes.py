"""Deployment routes (Blueprint v2 Section 2.4).

Phase 2 stubs: accept the locked request/response shape, return the
standard envelope. GitHub HMAC verification and XGBoost risk scoring
are wired up in Phase 6 — see R-69/R-77.
"""

from uuid import UUID, uuid4

from fastapi import APIRouter, Request, status

from app.deployment_risk.schemas import (
    DeploymentListResponse,
    DeploymentWebhookResponse,
)
from app.shared.types import ApiResponse

router = APIRouter(prefix="/deployments", tags=["Deployments"])


@router.post(
    "/webhook",
    response_model=ApiResponse[DeploymentWebhookResponse],
    status_code=status.HTTP_202_ACCEPTED,
    summary="GitHub Actions deployment webhook receiver",
)
async def deployment_webhook(
    request: Request,
) -> ApiResponse[DeploymentWebhookResponse]:
    """Phase 2 stub — HMAC signature verification (R-54) and XGBoost
    scoring are wired up in Phase 6. This stub only acknowledges receipt.
    """
    if await request.body():
        await request.json()
    return ApiResponse[DeploymentWebhookResponse](
        success=True,
        data=DeploymentWebhookResponse(
            deployment_id=uuid4(),
            risk_score=0.0,
            risk_explanation=None,
        ),
    )


@router.get(
    "",
    response_model=ApiResponse[DeploymentListResponse],
    summary="List deployments, optionally filtered by service",
)
async def list_deployments(
    service_id: UUID | None = None,
    limit: int = 50,
) -> ApiResponse[DeploymentListResponse]:
    """Phase 2 stub — reads from PostgreSQL are wired up in Phase 3."""
    return ApiResponse[DeploymentListResponse](
        success=True,
        data=DeploymentListResponse(deployments=[]),
    )
