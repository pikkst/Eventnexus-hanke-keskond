from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Request, status
from pydantic import BaseModel, Field

from app.version import __version__

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str = Field(description="Service status")
    timestamp: str = Field(description="ISO-8601 UTC timestamp")


class ReadinessResponse(BaseModel):
    status: str = Field(description="Readiness status")
    timestamp: str = Field(description="ISO-8601 UTC timestamp")
    version: str = Field(description="Application version")
    environment: str = Field(description="Deployment environment")


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


@router.get(
    "/health",
    operation_id="health",
    response_model=HealthResponse,
    summary="Liveness check",
    responses={status.HTTP_200_OK: {"description": "Service is alive"}},
)
async def health(request: Request) -> HealthResponse:
    return HealthResponse(
        status="ok",
        timestamp=_utc_now_iso(),
    )


@router.get(
    "/ready",
    operation_id="readiness",
    response_model=ReadinessResponse,
    summary="Readiness check",
    responses={status.HTTP_200_OK: {"description": "Service is ready"}},
    status_code=status.HTTP_200_OK,
)
async def ready(request: Request) -> ReadinessResponse:
    settings = request.app.state.settings
    return ReadinessResponse(
        status="ok",
        timestamp=_utc_now_iso(),
        version=__version__,
        environment=settings.app_env.value,
    )
