"""FastAPI middlewares for request-ID injection, security headers, and errors."""

import time
import uuid
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.shared.errors import SentinelError
from app.shared.logging import logger
from app.shared.types import ApiResponse, ErrorDetail, ResponseMeta

# Maps Starlette's default HTTP status codes to Blueprint v2 Section 2.4
# error codes. These fire for routing-level failures (unmatched path,
# wrong method) that never construct a SentinelError, so without this
# map they'd fall through to FastAPI's default {"detail": "..."} body
# instead of the standard envelope (Rule R-28 applies to every response,
# not just ones raised from application code).
_STATUS_CODE_MAP: dict[int, str] = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    422: "VALIDATION_ERROR",
    429: "RATE_LIMIT_EXCEEDED",
}


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Injects X-Request-ID header and binds correlation ID to request context."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        return response


def register_error_handlers(app: FastAPI) -> None:
    """Registers standard envelope error handlers for all exceptions (Rule R-28)."""

    @app.exception_handler(SentinelError)
    async def handle_sentinel_error(
        request: Request, exc: SentinelError
    ) -> JSONResponse:
        request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
        logger.warn(
            "sentinel_error",
            error_code=exc.code,
            message=exc.message,
            request_id=request_id,
        )
        body = ApiResponse[None](
            success=False,
            data=None,
            error=ErrorDetail(code=exc.code, message=exc.message, fields=exc.fields),
            meta=ResponseMeta(request_id=request_id),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=body.model_dump(mode="json"),
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        """Wraps FastAPI/Starlette's built-in HTTPExceptions in the envelope.

        Covers routing-level failures that never touch application code —
        unmatched paths (404), wrong HTTP methods (405), and any bare
        HTTPException(status_code=...) raised directly — none of which
        construct a SentinelError, so they'd otherwise bypass the
        envelope entirely and leak {"detail": "..."} to the client.
        """
        request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
        code = _STATUS_CODE_MAP.get(exc.status_code, "HTTP_ERROR")
        logger.warn(
            "http_exception",
            status_code=exc.status_code,
            error_code=code,
            request_id=request_id,
        )
        body = ApiResponse[None](
            success=False,
            data=None,
            error=ErrorDetail(code=code, message=str(exc.detail)),
            meta=ResponseMeta(request_id=request_id),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=body.model_dump(mode="json"),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Wraps Pydantic request-validation failures in the envelope.

        FastAPI raises this before a route handler ever runs (bad JSON
        body, missing required field, wrong type), so — like the 404/405
        case above — it never passes through application code and would
        otherwise return FastAPI's default {"detail": [...]} shape
        instead of the standard envelope's structured `error.fields`.
        """
        request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
        fields = [
            {"loc": ".".join(str(p) for p in err["loc"]), "msg": err["msg"]}
            for err in exc.errors()
        ]
        logger.warn(
            "validation_error",
            request_id=request_id,
            fields=fields,
        )
        body = ApiResponse[None](
            success=False,
            data=None,
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Request validation failed",
                fields=fields,
            ),
            meta=ResponseMeta(request_id=request_id),
        )
        return JSONResponse(
            status_code=422,
            content=body.model_dump(mode="json"),
        )

    @app.exception_handler(Exception)
    async def handle_unhandled_error(request: Request, exc: Exception) -> JSONResponse:
        request_id = getattr(request.state, "request_id", str(uuid.uuid4()))
        logger.error(
            "unhandled_error",
            error=str(exc),
            request_id=request_id,
        )
        body = ApiResponse[None](
            success=False,
            data=None,
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected server error occurred",
            ),
            meta=ResponseMeta(request_id=request_id),
        )
        return JSONResponse(
            status_code=500,
            content=body.model_dump(mode="json"),
        )
