from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import structlog
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.config import Settings
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
        })
    return safe


def _get_correlation_id(request: Request) -> str | None:
    return request.scope.get("correlation_id") or get_correlation_id()


def _cors_headers_for_origin(origin: str | None, settings: Settings) -> dict[str, str]:
    if not origin:
        return {}
    if origin not in settings.cors_origins:
        return {}
    headers: dict[str, str] = {
        "access-control-allow-origin": origin,
        "access-control-allow-methods": ", ".join(settings.cors_methods),
        "access-control-allow-headers": ", ".join(settings.cors_headers),
        "access-control-expose-headers": "X-Request-ID",
    }
    return headers


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        correlation_id = _get_correlation_id(request)
        is_production = request.app.state.app_env == "production"
        settings = request.app.state.settings

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

        headers: dict[str, str] = {}
        if correlation_id:
            headers[CORRELATION_HEADER] = correlation_id
        headers.update(_cors_headers_for_origin(request.headers.get("origin"), settings))

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=content,
            headers=headers,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        correlation_id = _get_correlation_id(request)
        settings = request.app.state.settings

        extra_headers: dict[str, str] = {}
        if exc.headers:
            for key, value in exc.headers.items():
                extra_headers[key] = value

        headers: dict[str, str] = {}
        if correlation_id:
            headers[CORRELATION_HEADER] = correlation_id
        headers.update(_cors_headers_for_origin(request.headers.get("origin"), settings))
        headers.update(extra_headers)

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail,
                "error_code": "http_error",
                "correlation_id": correlation_id,
            },
            headers=headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        correlation_id = _get_correlation_id(request)
        settings = request.app.state.settings
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

        headers: dict[str, str] = {}
        if correlation_id:
            headers[CORRELATION_HEADER] = correlation_id
        headers.update(_cors_headers_for_origin(request.headers.get("origin"), settings))

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Request validation failed",
                "error_code": "validation_error",
                "correlation_id": correlation_id,
                "errors": safe_errors,
            },
            headers=headers,
        )
