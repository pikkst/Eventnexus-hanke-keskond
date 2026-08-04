from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

import pytest
from fastapi import Body, FastAPI, Request
from httpx import ASGITransport, AsyncClient
from pydantic import BaseModel, Field, field_validator

from app.config import AppEnvironment, Settings
from app.main import create_app


def _make_test_settings(**overrides: object) -> Settings:
    defaults: dict[str, object] = {
        "app_env": AppEnvironment.TESTING,
        "debug": False,
        "secret_key": "test-secret-key-for-testing-purposes-only",
        "log_level": "DEBUG",
        "log_format": "console",
    }
    defaults.update(overrides)
    return Settings(**defaults)  # type: ignore[arg-type]


def _make_prod_settings(**overrides: object) -> Settings:
    defaults: dict[str, object] = {
        "app_env": AppEnvironment.PRODUCTION,
        "debug": False,
        "secret_key": "a-very-secure-secret-key-with-32-chars!",
        "log_level": "INFO",
        "log_format": "json",
    }
    defaults.update(overrides)
    return Settings(**defaults)  # type: ignore[arg-type]


class _BodySchema(BaseModel):
    name: str = Field(min_length=1)


class _CustomValidatorSchema(BaseModel):
    code: str

    @field_validator("code")
    @classmethod
    def validate_code_format(cls, v: str) -> str:
        if not v.startswith("EV-"):
            raise ValueError("Code must start with EV-")
        return v


def _add_test_routes(app: FastAPI) -> None:
    @app.get("/test/error")
    async def raise_error(request: Request) -> None:
        raise RuntimeError("Test error message")

    @app.post("/test/validation")
    async def validation_error(
        data: Annotated[_BodySchema, Body()],
    ) -> _BodySchema:
        return data

    @app.post("/test/custom-validation")
    async def custom_validation_error(
        data: Annotated[_CustomValidatorSchema, Body()],
    ) -> _CustomValidatorSchema:
        return data


@pytest.fixture
def test_settings() -> Settings:
    return _make_test_settings()


@pytest.fixture
def prod_settings() -> Settings:
    return _make_prod_settings()


@pytest.fixture
def test_app(test_settings: Settings) -> FastAPI:
    app = create_app(settings=test_settings)
    _add_test_routes(app)
    return app


@pytest.fixture
def prod_app(prod_settings: Settings) -> FastAPI:
    app = create_app(settings=prod_settings)
    _add_test_routes(app)
    return app


@pytest.fixture
async def test_client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=test_app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://localhost") as client:
        yield client


@pytest.fixture
async def prod_client(prod_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=prod_app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://127.0.0.1") as client:
        yield client
