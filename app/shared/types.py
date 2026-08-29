"""Shared Pydantic models, TypedDicts, and standard response envelopes (Rule R-33)."""

from datetime import datetime, timezone
from typing import Any, Generic, Optional, TypeVar
from uuid import uuid4

from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """Structured error object inside standard response envelope."""

    code: str
    message: str
    fields: Optional[list[dict[str, Any]]] = None


class ResponseMeta(BaseModel):
    """Metadata envelope present in every API response."""

    version: str = "v1"
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response envelope for all endpoints (Rule R-28)."""

    success: bool
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


class HealthStatus(BaseModel):
    """System health check payload."""

    status: str
    services: Optional[dict[str, str]] = None
