from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import redis
from fastapi import APIRouter, Request, status
from pydantic import BaseModel, Field

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str = Field(description="Service status")
    timestamp: str = Field(description="ISO-8601 UTC timestamp")


class DependencyStatus(BaseModel):
    name: str = Field(description="Dependency name")
    status: str = Field(description="Dependency status")
    details: dict[str, Any] | None = Field(default=None, description="Optional dependency details")


class ReadinessResponse(BaseModel):
    status: str = Field(description="Readiness status")
    timestamp: str = Field(description="ISO-8601 UTC timestamp")
    version: str = Field(description="Application version")
    environment: str = Field(description="Deployment environment")
    dependencies: list[DependencyStatus] = Field(default_factory=list, description="Dependency health checks")


def _utc_now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _check_redis(settings: Any) -> DependencyStatus:
    try:
        client = redis.Redis(
            host=settings.worker_redis_host,
            port=settings.worker_redis_port,
            db=settings.worker_redis_db,
            password=settings.worker_redis_password or None,
            socket_timeout=2,
            socket_connect_timeout=2,
        )
        client.ping()
        client.close()
        return DependencyStatus(
            name="redis",
            status="connected",
            details={
                "host": settings.worker_redis_host,
                "port": settings.worker_redis_port,
                "db": settings.worker_redis_db,
            },
        )
    except Exception as exc:  # noqa: BLE001
        return DependencyStatus(
            name="redis",
            status="unreachable",
            details={"error": str(exc)},
        )


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
    operation_id="ready",
    response_model=ReadinessResponse,
    summary="Readiness check",
    responses={status.HTTP_200_OK: {"description": "Service is ready"}},
    status_code=status.HTTP_200_OK,
)
async def ready(request: Request) -> ReadinessResponse:
    settings = request.app.state.settings
    dependencies = [
        _check_redis(settings),
    ]

    all_healthy = all(dep.status == "connected" for dep in dependencies)
    overall_status = "ready" if all_healthy else "degraded"

    return ReadinessResponse(
        status=overall_status,
        timestamp=_utc_now_iso(),
        version=settings.app_version,
        environment=settings.app_env.value,
        dependencies=dependencies,
    )
