"""FastAPI middlewares for request-ID injection, security headers, and errors."""

import time
import uuid
from typing import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.shared.errors import SentinelError
from app.shared.logging import logger
from app.shared.types import ApiResponse, ErrorDetail, ResponseMeta


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
