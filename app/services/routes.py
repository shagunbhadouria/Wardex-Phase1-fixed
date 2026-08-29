"""Service and metric routes (Blueprint v2 Section 2.4).

Phase 2 stubs: accept the locked request/response shape, return the
standard envelope. No DB reads/writes yet (Phase 3), no Isolation
Forest scoring yet (Phase 6) — see R-69/R-77.
"""

from uuid import UUID

from fastapi import APIRouter, status

from app.services.schemas import (
    MetricIngestionResponse,
    MetricListResponse,
    MetricSnapshotCreate,
    ServiceCreate,
    ServiceListResponse,
    ServiceResponse,
)
from app.shared.types import ApiResponse

router = APIRouter(prefix="/services", tags=["Services"])


@router.get(
    "",
    response_model=ApiResponse[ServiceListResponse],
    summary="List all connected services",
)
async def list_services() -> ApiResponse[ServiceListResponse]:
    """Phase 2 stub — reads from PostgreSQL are wired up in Phase 3."""
    return ApiResponse[ServiceListResponse](
        success=True,
        data=ServiceListResponse(services=[]),
    )


@router.post(
    "",
    response_model=ApiResponse[ServiceResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new service",
)
async def create_service(payload: ServiceCreate) -> ApiResponse[ServiceResponse]:
    """Phase 2 stub — persistence is wired up in Phase 3."""
    from datetime import datetime, timezone
    from uuid import uuid4

    return ApiResponse[ServiceResponse](
        success=True,
        data=ServiceResponse(
            id=uuid4(),
            name=payload.name,
            environment=payload.environment,
            baseline_cpu=0.0,
            baseline_memory=0.0,
            baseline_error_rate=0.0,
            created_at=datetime.now(timezone.utc),
        ),
    )


@router.get(
    "/{service_id}/metrics",
    response_model=ApiResponse[MetricListResponse],
    summary="Get recent metric snapshots for a service",
)
async def get_service_metrics(
    service_id: UUID,
) -> ApiResponse[MetricListResponse]:
    """Phase 2 stub — reads from PostgreSQL are wired up in Phase 3."""
    return ApiResponse[MetricListResponse](
        success=True,
        data=MetricListResponse(metrics=[]),
    )


@router.post(
    "/{service_id}/metrics",
    response_model=ApiResponse[MetricIngestionResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Ingest a metric snapshot for a service",
)
async def ingest_service_metrics(
    service_id: UUID,
    payload: MetricSnapshotCreate,
) -> ApiResponse[MetricIngestionResponse]:
    """Phase 2 stub — persistence, Celery dispatch, and Isolation Forest
    scoring are wired up in Phases 3/5/6. This stub only validates the
    request shape and acknowledges receipt.
    """
    return ApiResponse[MetricIngestionResponse](
        success=True,
        data=MetricIngestionResponse(
            snapshot_id=None,
            service_id=service_id,
            anomaly_detected=False,
            status="received",
        ),
    )
