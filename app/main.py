"""FastAPI application factory and lifecycle management."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.routes import router as auth_router
from app.chaos.routes import router as chaos_router
from app.config import settings
from app.deployment_risk.routes import router as deployments_router
from app.incident_analysis.routes import router as incidents_router
from app.services.routes import router as services_router
from app.shared.logging import logger, setup_logging
from app.shared.middleware import RequestIdMiddleware, register_error_handlers
from app.shared.types import ApiResponse, HealthStatus

API_V1_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown lifecycle handler."""
    setup_logging(settings.LOG_LEVEL)
    logger.info(
        "app.startup",
        environment=settings.ENVIRONMENT,
        version="1.0.0",
    )
    yield
    logger.info("app.shutdown")


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application instance."""
    app = FastAPI(
        title="SentinelAI",
        description="Autonomous Operational Intelligence Platform",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_URL, "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RequestIdMiddleware)
    register_error_handlers(app)

    # Versioned routers — Blueprint v2 Section 2.4: base URL is /api/v1/.
    # All 13 route stubs are now registered (Phase 2 — Backend Skeleton).
    # Every handler returns the standard envelope with placeholder/empty
    # data; real DB reads (Phase 3), auth (Phase 4), Celery dispatch and
    # ML scoring (Phase 5-6), and LLM analysis (Phase 7) are wired up in
    # their respective phases — see R-69/R-77. /health is deliberately
    # unversioned (v2's endpoint table lists it as GET /health, no
    # prefix) since load balancers and container orchestrators probe it
    # and shouldn't need to track API versions.
    app.include_router(auth_router, prefix=API_V1_PREFIX)
    app.include_router(services_router, prefix=API_V1_PREFIX)
    app.include_router(deployments_router, prefix=API_V1_PREFIX)
    app.include_router(incidents_router, prefix=API_V1_PREFIX)
    app.include_router(chaos_router, prefix=API_V1_PREFIX)

    @app.get(
        "/health",
        response_model=ApiResponse[HealthStatus],
        summary="Health Check Endpoint",
        tags=["System"],
    )
    async def health_check() -> ApiResponse[HealthStatus]:
        """Returns application startup and connectivity health status."""
        # TECH DEBT: OBS-001 — /health returns a hardcoded status and does
        # not check db/redis/celery/groq connectivity, unlike the shape
        # specified in Blueprint v2 Section 2.4 ({ status, services: { db,
        # redis, celery, groq } }). This is a stub: those clients don't
        # exist yet. Wire real connectivity checks in Phase 5 (Ingestion
        # Pipeline) once the DB/Redis/Celery clients are built — see R-89.
        return ApiResponse[HealthStatus](
            success=True,
            data=HealthStatus(
                status="starting",
                services={"api": "healthy"},
            ),
        )

    return app


app = create_app()
