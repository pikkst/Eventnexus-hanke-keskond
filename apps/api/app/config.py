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
