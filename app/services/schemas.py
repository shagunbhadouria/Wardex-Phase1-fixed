"""Pydantic schemas for service and metric routes (Blueprint v2 Section 2.4)."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ServiceCreate(BaseModel):
    """Request body for POST /services."""

    name: str
    environment: str = "production"


class ServiceResponse(BaseModel):
    """A single service record."""

    id: UUID
    name: str
    environment: str
    baseline_cpu: float
    baseline_memory: float
    baseline_error_rate: float
    created_at: datetime


class ServiceListResponse(BaseModel):
    """Response payload for GET /services."""

    services: list[ServiceResponse]


class MetricSnapshotCreate(BaseModel):
    """Request body for POST /services/:id/metrics."""

    cpu_percent: float
    memory_percent: float
    error_rate: float
    api_latency_ms: float
    request_count: int = 0


class MetricSnapshotResponse(BaseModel):
    """A single metric snapshot record."""

    id: int
    service_id: UUID
    cpu_percent: float
    memory_percent: float
    error_rate: float
    api_latency_ms: float
    request_count: int
    anomaly_score: Optional[float] = None
    is_anomalous: bool = False
    recorded_at: datetime


class MetricListResponse(BaseModel):
    """Response payload for GET /services/:id/metrics."""

    metrics: list[MetricSnapshotResponse]


class MetricIngestionResponse(BaseModel):
    """Response payload for POST /services/:id/metrics."""

    snapshot_id: Optional[int] = None
    service_id: UUID
    anomaly_detected: bool = False
    status: str = "received"
