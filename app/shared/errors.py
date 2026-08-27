"""Custom exceptions and standard error codes for SentinelAI."""

from typing import Any, Optional


class SentinelError(Exception):
    """Base exception for all SentinelAI domain errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_SERVER_ERROR",
        status_code: int = 500,
        fields: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.fields = fields or []


class ValidationError(SentinelError):
    """Raised when request payload or entity validation fails."""

    def __init__(
        self,
        message: str,
        fields: Optional[list[dict[str, Any]]] = None,
    ) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
            fields=fields,
        )


class UnauthorizedError(SentinelError):
    """Raised when authentication credentials are missing or invalid."""

    def __init__(
        self, message: str = "Unauthorized", code: str = "UNAUTHORIZED"
    ) -> None:
        super().__init__(message=message, code=code, status_code=401)


class ForbiddenError(SentinelError):
    """Raised when user or service lacks required permissions."""

    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message=message, code="FORBIDDEN", status_code=403)


class NotFoundError(SentinelError):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message=message, code="NOT_FOUND", status_code=404)


class RateLimitExceededError(SentinelError):
    """Raised when request rate exceeds allowed quota."""

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        super().__init__(
            message=message,
            code="RATE_LIMIT_EXCEEDED",
            status_code=429,
        )
