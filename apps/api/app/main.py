from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.errors import register_error_handlers
from app.api.routes import api_router
from app.config import Settings, get_settings
from app.core.correlation import CorrelationIdMiddleware
from app.core.logging import configure_logging
from app.version import __version__

_TAGS_METADATA = [
    {
        "name": "health",
        "description": "Service liveness and readiness checks",
    },
]


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = get_settings()

    configure_logging(settings)
    logger = structlog.get_logger("eventnexus.api")

    logger.info(
        "Starting application",
        **settings.to_safe_dict(),
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        logger.info("Application started successfully")
        yield
        logger.info("Application shutting down")

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description=(
            "EventNexus Hanke Keskond API — procurement intelligence "
            "and tender preparation for Eventnexus OÜ."
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
        servers=[{"url": "http://localhost:8000", "description": "Local development"}],
        lifespan=lifespan,
    )

    app.state.app_env = settings.app_env.value
    app.state.settings = settings
    app.state.debug = settings.debug

    register_error_handlers(app)

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.allowed_hosts,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=False,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
    app.add_middleware(CorrelationIdMiddleware)

    app.include_router(api_router)

    return app


def run() -> None:
    settings = get_settings()
    uvicorn.run(
        app="app.main:create_app",
        factory=True,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
    )


app = create_app()
