from __future__ import annotations

import logging
from enum import StrEnum
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvironment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = Field(
        default="EventNexus Hanke Keskond",
        description="Application name shown in OpenAPI and logs",
    )
    app_version: str = Field(default="0.1.0")
    app_env: AppEnvironment = Field(
        default=AppEnvironment.DEVELOPMENT,
        description="Application environment",
    )
    debug: bool = Field(default=False, description="Enable debug mode")

    api_host: str = Field(default="0.0.0.0", description="API bind host")
    api_port: int = Field(default=8000, ge=1, le=65535, description="API bind port")

    secret_key: str = Field(
        default="",
        description="Secret key for session/token signing (required in production)",
    )

    log_level: str = Field(default="info", description="Log level")
    log_format: str = Field(default="json", description="Log format: json or console")

    allowed_hosts: list[str] = Field(
        default_factory=lambda: ["localhost", "127.0.0.1", "::1"],
        description="Trusted host allowlist",
    )

    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"],
        description="CORS allowed origins",
    )

    cors_methods: list[str] = Field(
        default_factory=lambda: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        description="CORS allowed methods",
    )

    cors_headers: list[str] = Field(
        default_factory=lambda: ["Authorization", "Content-Type", "X-Requested-With"],
        description="CORS allowed headers",
    )

    @field_validator("log_level", mode="before")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        if isinstance(v, str):
            level = v.upper()
            if level not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
                raise ValueError(
                    f"Invalid log level '{v}'. Must be one of: "
                    "DEBUG, INFO, WARNING, ERROR, CRITICAL"
                )
            return level
        return v

    @field_validator("log_format", mode="before")
    @classmethod
    def validate_log_format(cls, v: str) -> str:
        if isinstance(v, str):
            fmt = v.lower()
            if fmt not in ("json", "console"):
                raise ValueError(
                    f"Invalid log format '{v}'. Must be 'json' or 'console'"
                )
            return fmt
        return v

    @field_validator("allowed_hosts", mode="before")
    @classmethod
    def validate_allowed_hosts(cls, v: list[str] | str | None) -> list[str]:
        if v is None:
            return ["localhost", "127.0.0.1", "::1"]
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    @field_validator("cors_origins", mode="before")
    @classmethod
    def validate_cors_origins(cls, v: list[str] | str | None) -> list[str]:
        if v is None:
            return ["http://localhost:3000", "http://127.0.0.1:3000"]
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    @field_validator("cors_methods", mode="before")
    @classmethod
    def validate_cors_methods(cls, v: list[str] | str | None) -> list[str]:
        if v is None:
            return ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
        if isinstance(v, str):
            return [item.strip().upper() for item in v.split(",") if item.strip()]
        return v

    @field_validator("cors_headers", mode="before")
    @classmethod
    def validate_cors_headers(cls, v: list[str] | str | None) -> list[str]:
        if v is None:
            return ["Authorization", "Content-Type", "X-Requested-With"]
        if isinstance(v, str):
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

    @model_validator(mode="after")
    def validate_critical_settings(self) -> Settings:
        if self.app_env == AppEnvironment.PRODUCTION:
            if not self.secret_key or len(self.secret_key) < 32:
                raise ValueError(
                    "SECRET_KEY must be set and at least 32 characters long "
                    "when APP_ENV=production"
                )
            if self.debug:
                raise ValueError("DEBUG must be false when APP_ENV=production")
            if "*" in self.allowed_hosts:
                raise ValueError(
                    "ALLOWED_HOSTS must not contain '*' when APP_ENV=production"
                )
            if "*" in self.cors_origins:
                raise ValueError(
                    "CORS_ORIGINS must not contain '*' when APP_ENV=production"
                )
        return self

    def is_production(self) -> bool:
        return self.app_env == AppEnvironment.PRODUCTION

    def is_testing(self) -> bool:
        return self.app_env == AppEnvironment.TESTING

    def get_log_level(self) -> int:
        level: int = getattr(logging, self.log_level.upper())
        return level

    def to_safe_dict(self) -> dict[str, Any]:
        """Return a sanitized dict for logging that excludes secrets."""
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "app_env": self.app_env.value,
            "api_host": self.api_host,
            "api_port": self.api_port,
            "log_level": self.log_level,
            "log_format": self.log_format,
            "debug": self.debug,
        }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


@lru_cache(maxsize=1)
def get_settings_path() -> Path:
    cwd = Path.cwd()
    return (cwd / ".env").resolve()
