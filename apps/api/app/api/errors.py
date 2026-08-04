from __future__ import annotations

from typing import Any

import structlog
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.core.correlation import CORRELATION_HEADER, get_correlation_id

logger = structlog.get_logger("eventnexus.api")


def _correlation_headers(correlation_id: str | None) -> dict[str, str]:
    headers: dict[str, str] = {}
    if correlation_id:
        headers[CORRELATION_HEADER] = correlation_id
    return headers


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        correlation_id = get_correlation_id()
        is_production = request.app.state.app_env == "production"

        logger.error(
            "Unhandled exception",
            error_type=type(exc).__name__,
            error_message=str(exc),
            path=request.url.path,
            method=request.method,
            correlation_id=correlation_id,
            exc_info=exc,
        )

        content: dict[str, Any]
        if is_production:
            content = {
                "detail": "Internal server error",
                "error_code": "internal_error",
                "correlation_id": correlation_id,
            }
        else:
            content = {
                "detail": str(exc),
                "error_code": "internal_error",
                "correlation_id": correlation_id,
            }

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=content,
            headers=_correlation_headers(correlation_id),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        correlation_id = get_correlation_id()

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "error_code": "http_error",
                "correlation_id": correlation_id,
            },
            headers=_correlation_headers(correlation_id),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        correlation_id = get_correlation_id()
        errors = exc.errors()

        logger.warning(
            "Request validation failed",
            path=request.url.path,
            method=request.method,
            errors=errors,
            correlation_id=correlation_id,
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Request validation failed",
                "error_code": "validation_error",
                "correlation_id": correlation_id,
                "errors": errors,
            },
            headers=_correlation_headers(correlation_id),
        )
