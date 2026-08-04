from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import structlog
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.core.correlation import CORRELATION_HEADER, get_correlation_id

logger = structlog.get_logger("eventnexus.api")


def _safe_validation_errors(errors: Sequence[Any]) -> list[dict[str, Any]]:
    safe: list[dict[str, Any]] = []
    for error in errors:
        if not isinstance(error, dict):
            continue
        safe_error: dict[str, Any] = {
            "type": error.get("type", ""),
            "loc": error.get("loc", []),
            "msg": error.get("msg", ""),
            "input": "<redacted>",
        }
        ctx = error.get("ctx")
        if isinstance(ctx, dict):
            safe_ctx: dict[str, Any] = {}
            for key, value in ctx.items():
                if isinstance(value, (str, int, float, bool)):
                    safe_ctx[key] = value
                else:
                    safe_ctx[key] = "<non-serializable>"
            safe_error["ctx"] = safe_ctx
        safe.append(safe_error)
    return safe


def _safe_errors_for_logging(errors: Sequence[Any]) -> list[dict[str, Any]]:
    safe: list[dict[str, Any]] = []
    for error in errors:
        if not isinstance(error, dict):
            continue
        safe.append({
            "type": error.get("type", ""),
            "loc": error.get("loc", []),
            "msg": error.get("msg", ""),
        })
    return safe


def _merge_correlation_headers(correlation_id: str | None, extra_headers: dict[str, str] | None) -> dict[str, str]:
    headers: dict[str, str] = {}
    if correlation_id:
        headers[CORRELATION_HEADER] = correlation_id
    if extra_headers:
        headers.update(extra_headers)
    return headers


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

        extra_headers: dict[str, str] = {}
        if exc.headers:
            for key, value in exc.headers.items():
                extra_headers[key] = value

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "error_code": "http_error",
                "correlation_id": correlation_id,
            },
            headers=_merge_correlation_headers(correlation_id, extra_headers),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        correlation_id = get_correlation_id()
        raw_errors = exc.errors()
        safe_errors = _safe_validation_errors(raw_errors)
        log_errors = _safe_errors_for_logging(raw_errors)

        logger.warning(
            "Request validation failed",
            path=request.url.path,
            method=request.method,
            errors=log_errors,
            correlation_id=correlation_id,
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Request validation failed",
                "error_code": "validation_error",
                "correlation_id": correlation_id,
                "errors": safe_errors,
            },
            headers=_correlation_headers(correlation_id),
        )
