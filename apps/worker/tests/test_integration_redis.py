from __future__ import annotations

import socket

import pytest

from app.config import AppEnvironment, Settings
from app.health import _check_redis


def _is_redis_available(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False


def _make_test_settings(**overrides: object) -> Settings:
    defaults: dict[str, object] = {
        "app_env": AppEnvironment.TESTING,
        "debug": False,
        "worker_redis_host": "localhost",
        "worker_redis_port": 6379,
        "worker_redis_db": 0,
        "worker_redis_password": "",
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


@pytest.mark.skipif(
    not _is_redis_available("localhost", 6379),
    reason="Redis is not running on localhost:6379",
)
class TestRedisIntegration:
    def test_redis_connectivity_check_returns_connected(self) -> None:
        settings = _make_test_settings()
        status = _check_redis(settings)
        assert status.name == "redis"
        assert status.status == "connected"
        assert status.details is not None
        assert status.details["host"] == "localhost"
        assert status.details["port"] == 6379

    def test_redis_connectivity_check_includes_db(self) -> None:
        settings = _make_test_settings(worker_redis_db=1)
        status = _check_redis(settings)
        assert status.status == "connected"
        assert status.details is not None
        assert status.details["db"] == 1
