from __future__ import annotations

import logging
from enum import StrEnum
from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvironment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class QueueName(StrEnum):
    DEFAULT = "default"
    HIGH = "high"
    LOW = "low"
    DEAD_LETTER = "dead_letter"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_name: str = Field(
        default="EventNexus Hanke Keskond Worker",
        description="Application name shown in logs",
    )
    app_version: str = Field(default="0.1.0")
    app_env: AppEnvironment = Field(
        default=AppEnvironment.DEVELOPMENT,
        description="Application environment",
    )
    debug: bool = Field(default=False, description="Enable debug mode")

    worker_redis_host: str = Field(default="localhost", description="Redis host")
    worker_redis_port: int = Field(default=6379, ge=1, le=65535, description="Redis port")
    worker_redis_db: int = Field(default=0, ge=0, le=15, description="Redis database")
    worker_redis_password: str = Field(default="", description="Redis password")

    worker_threads: int = Field(default=4, ge=1, le=50, description="Worker thread count")
    worker_processes: int = Field(default=1, ge=1, le=8, description="Worker process count")
    worker_queues: str = Field(default="default,high,low", description="Comma-separated queue names")

    worker_task_timeout: int = Field(default=60000, ge=1000, description="Task timeout in milliseconds")
    worker_max_retries: int = Field(default=3, ge=0, le=10, description="Maximum retries per task")
    worker_retry_delay: int = Field(default=5000, ge=0, description="Retry delay in milliseconds")
    worker_dead_letter_queue: str = Field(default="dead_letter", description="Dead letter queue name")

    worker_health_port: int = Field(default=8001, ge=1, le=65535, description="Health check port")

    log_level: str = Field(default="info", description="Log level")
    log_format: str = Field(default="json", description="Log format: json or console")

    @field_validator("debug", mode="before")
    @classmethod
    def validate_debug(cls, v: str | bool) -> bool:
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return False

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

    @field_validator("worker_queues", mode="before")
    @classmethod
    def validate_worker_queues(cls, v: str) -> str:
        if isinstance(v, str):
            queues = [q.strip() for q in v.split(",") if q.strip()]
            if not queues:
                raise ValueError("At least one worker queue must be configured")
            return ",".join(queues)
        return v

    @model_validator(mode="after")
    def validate_critical_settings(self) -> Settings:
        if self.app_env == AppEnvironment.PRODUCTION and self.debug:
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
            "worker_threads": self.worker_threads,
            "worker_processes": self.worker_processes,
            "worker_queues": self.worker_queues,
            "worker_max_retries": self.worker_max_retries,
            "worker_task_timeout": self.worker_task_timeout,
            "worker_dead_letter_queue": self.worker_dead_letter_queue,
            "log_level": self.log_level,
            "log_format": self.log_format,
            "debug": self.debug,
        }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
