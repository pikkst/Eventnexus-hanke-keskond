from __future__ import annotations

import threading
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import dramatiq
import structlog
import uvicorn
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import AgeLimit, TimeLimit
from dramatiq.worker import Worker
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.config import Settings, get_settings
from app.core.logging import configure_logging
from app.core.middleware import DeadLetterMiddleware
from app.health import router as health_router
from app.jobs import run_sample_job

logger = structlog.get_logger("eventnexus.worker")

_TAGS_METADATA = [
    {
        "name": "health",
        "description": "Service liveness and readiness checks",
    },
    {
        "name": "jobs",
        "description": "Job management endpoints",
    },
]


class EnqueueJobRequest(BaseModel):
    idempotency_key: str = Field(..., min_length=1, description="Unique idempotency key")
    payload: dict[str, object] = Field(default_factory=dict, description="Arbitrary job payload")
    simulate_failure: bool = Field(default=False, description="Simulate a processing failure")


def _create_broker(settings: Settings) -> RedisBroker:
    broker = RedisBroker(  # type: ignore[no-untyped-call]
        host=settings.worker_redis_host,
        port=settings.worker_redis_port,
        db=settings.worker_redis_db,
        password=settings.worker_redis_password or None,
    )
    broker.middleware = [
        m for m in broker.middleware
        if type(m).__name__ not in ("TimeLimit", "AgeLimit")
    ]
    broker.add_middleware(DeadLetterMiddleware(
        dead_letter_queue_name=settings.worker_dead_letter_queue,
        max_retries=settings.worker_max_retries,
    ))
    broker.add_middleware(TimeLimit(time_limit=settings.worker_task_timeout))
    broker.add_middleware(AgeLimit(max_age=86400000))
    return broker


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = get_settings()

    configure_logging(settings)
    logger.info(
        "Starting worker application",
        **settings.to_safe_dict(),
    )

    broker = _create_broker(settings)
    dramatiq.set_broker(broker)

    sample_job_actor = dramatiq.actor(
        queue_name="default",
        priority=0,
        max_retries=settings.worker_max_retries,
        time_limit=settings.worker_task_timeout,
        broker=broker,
    )(run_sample_job)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        worker = Worker(broker, worker_threads=settings.worker_threads)
        thread = threading.Thread(target=worker.start, daemon=True)
        thread.start()
        logger.info(
            "Worker started",
            threads=settings.worker_threads,
            queues=settings.worker_queues,
        )
        yield
        worker.stop()
        thread.join(timeout=5)
        logger.info("Worker stopped")

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "EventNexus Hanke Keskond Worker — background job processing "
            "for procurement intelligence and tender preparation."
        ),
        contact={
            "name": "Eventnexus OÜ",
        },
        license_info={
            "name": "Proprietary",
        },
        openapi_tags=_TAGS_METADATA,
        docs_url="/docs",
        redoc_url="/redoc",
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.state.app_env = settings.app_env.value
    app.state.settings = settings
    app.state.debug = settings.debug

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "::1"],
    )

    app.include_router(health_router)

    @app.post(
        "/jobs/sample",
        operation_id="enqueue_sample_job",
        tags=["jobs"],
        summary="Enqueue sample idempotent job",
        response_model=dict[str, object],
    )
    async def enqueue_sample_job(
        request: Request,
        body: EnqueueJobRequest,
    ) -> dict[str, object]:
        message = sample_job_actor.send(
            idempotency_key=body.idempotency_key,
            payload=body.payload,
            simulate_failure=body.simulate_failure,
        )
        logger.info(
            "Sample job enqueued",
            message_id=message.message_id,
            idempotency_key=body.idempotency_key,
        )
        return {"message_id": message.message_id, "status": "enqueued"}

    return app


def run() -> None:
    settings = get_settings()
    uvicorn.run(
        app="app.main:create_app",
        factory=True,
        host="0.0.0.0",
        port=settings.worker_health_port,
        log_level=settings.log_level.lower(),
    )


app = create_app()
