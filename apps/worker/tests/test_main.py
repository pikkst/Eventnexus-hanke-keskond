from __future__ import annotations

from fastapi import FastAPI

from app.config import AppEnvironment, Settings
from app.main import create_app


def _make_test_settings(**overrides: object) -> Settings:
    defaults: dict[str, object] = {
        "app_env": AppEnvironment.TESTING,
        "debug": False,
        "worker_redis_host": "localhost",
        "worker_redis_port": 6379,
        "worker_redis_db": 0,
        "worker_threads": 2,
        "worker_max_retries": 3,
        "worker_task_timeout": 60000,
        "worker_dead_letter_queue": "dead_letter",
        "worker_health_port": 8001,
        "log_level": "DEBUG",
        "log_format": "console",
    }
    defaults.update(overrides)
    return Settings(**defaults)  # type: ignore[arg-type]


def test_import_main() -> None:
    settings = _make_test_settings()
    app = create_app(settings=settings)
    assert isinstance(app, FastAPI)
