from __future__ import annotations

import re
import uuid
from collections.abc import MutableMapping
from contextvars import ContextVar
from typing import Any

from starlette.types import ASGIApp, Receive, Scope, Send

correlation_id_ctx: ContextVar[str | None] = ContextVar("correlation_id", default=None)

CORRELATION_HEADER = "x-request-id"

_REQUEST_ID_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9\-._]{0,255}$")


def _sanitize_request_id(request_id: str) -> str:
    if not _REQUEST_ID_PATTERN.match(request_id):
        raise ValueError("Invalid request ID format")
    return request_id


def get_correlation_id() -> str | None:
    return correlation_id_ctx.get()


class CorrelationIdMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        raw_request_id = headers.get(CORRELATION_HEADER.encode(), b"").decode()

        if raw_request_id:
            try:
                request_id = _sanitize_request_id(raw_request_id)
            except ValueError:
                request_id = uuid.uuid4().hex
        else:
            request_id = uuid.uuid4().hex

        token = correlation_id_ctx.set(request_id)

        async def send_with_id(message: MutableMapping[str, Any]) -> None:
            if message["type"] == "http.response.start":
                response_headers = list(message.get("headers", []))
                normalized = [
                    header
                    for header in response_headers
                    if header[0].lower() != CORRELATION_HEADER.encode()
                ]
                normalized.append(
                    (CORRELATION_HEADER.encode(), request_id.encode())
                )
                message["headers"] = normalized
            await send(message)
            if message["type"] == "http.response.body":
                body = dict(message)
                if not body.get("more_body", False):
                    correlation_id_ctx.reset(token)

        await self.app(scope, receive, send_with_id)
