from __future__ import annotations

import pytest
from dramatiq.middleware import TimeLimit

from app.config import AppEnvironment, Settings
from app.core.middleware import DeadLetterMiddleware
from app.jobs import _idempotency_store, run_sample_job
from app.main import _create_broker


def _make_test_settings(**overrides: object) -> Settings:
    defaults: dict[str, object] = {
        "app_env": AppEnvironment.TESTING,
        "debug": False,
        "worker_redis_host": "localhost",
        "worker_redis_port": 6379,
        "worker_redis_db": 0,
        "worker_redis_password": "",
        "worker_threads": 2,
        "worker_processes": 1,
        "worker_queues": "default,high,low",
        "worker_task_timeout": 60000,
        "worker_max_retries": 3,
        "worker_retry_delay": 5000,
        "worker_dead_letter_queue": "dead_letter",
        "worker_health_port": 8001,
        "log_level": "DEBUG",
        "log_format": "console",
    }
    defaults.update(overrides)
    return Settings(**defaults)  # type: ignore[arg-type]


@pytest.fixture(autouse=True)
def _clear_idempotency_store() -> None:  # type: ignore[misc]
    _idempotency_store.clear()
    yield
    _idempotency_store.clear()


class TestRetryAndTimeoutBehavior:
    def test_max_retries_middleware_configured(self) -> None:
        settings = _make_test_settings(worker_max_retries=3)
        broker = _create_broker(settings)
        mw_types = [type(m) for m in broker.middleware]
        assert DeadLetterMiddleware in mw_types
        mw = next(m for m in broker.middleware if isinstance(m, DeadLetterMiddleware))
        assert mw.max_retries == 3

    def test_time_limit_middleware_configured(self) -> None:
        settings = _make_test_settings(worker_task_timeout=60000)
        broker = _create_broker(settings)
        mw_types = [type(m) for m in broker.middleware]
        assert TimeLimit in mw_types
        mw = next(m for m in broker.middleware if isinstance(m, TimeLimit))
        assert mw.time_limit == 60000

    def test_dead_letter_middleware_configured(self) -> None:
        settings = _make_test_settings(worker_dead_letter_queue="dead_letter")
        broker = _create_broker(settings)
        mw_types = [type(m) for m in broker.middleware]
        assert DeadLetterMiddleware in mw_types

    def test_idempotent_job_does_not_duplicate_on_retry(self) -> None:
        _idempotency_store.clear()
        result1 = run_sample_job(
            idempotency_key="retry-key",
            payload={"attempt": 1},
            simulate_failure=False,
        )
        result2 = run_sample_job(
            idempotency_key="retry-key",
            payload={"attempt": 2},
            simulate_failure=False,
        )
        assert result1["job_id"] == result2["job_id"]
        assert result1["processed_at"] == result2["processed_at"]
