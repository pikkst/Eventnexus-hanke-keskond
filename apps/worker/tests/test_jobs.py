from __future__ import annotations

import pytest

from app.config import AppEnvironment, Settings
from app.jobs import _idempotency_store, run_sample_job


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


@pytest.fixture(autouse=True)
def _clear_idempotency_store() -> None:  # type: ignore[misc]
    _idempotency_store.clear()
    yield
    _idempotency_store.clear()


class TestSampleIdempotentJob:
    async def test_job_processes_successfully(self) -> None:
        result = run_sample_job(
            idempotency_key="key-1",
            payload={"task": "test"},
            simulate_failure=False,
        )
        assert result["status"] == "processed"
        assert result["idempotency_key"] == "key-1"
        assert result["payload"] == {"task": "test"}

    async def test_duplicate_execution_returns_same_result(self) -> None:
        result1 = run_sample_job(
            idempotency_key="key-dup",
            payload={"task": "test"},
            simulate_failure=False,
        )
        result2 = run_sample_job(
            idempotency_key="key-dup",
            payload={"task": "test"},
            simulate_failure=False,
        )
        assert result1["job_id"] == result2["job_id"]
        assert result1["status"] == result2["status"]
        assert result1["processed_at"] == result2["processed_at"]

    async def test_simulated_failure_raises_error(self) -> None:
        with pytest.raises(RuntimeError, match="Simulated processing failure"):
            run_sample_job(
                idempotency_key="key-fail",
                payload={},
                simulate_failure=True,
            )

    async def test_different_keys_produce_different_results(self) -> None:
        result1 = run_sample_job(idempotency_key="key-a", payload={"v": 1})
        result2 = run_sample_job(idempotency_key="key-b", payload={"v": 2})
        assert result1["job_id"] != result2["job_id"]
        assert result1["payload"] == {"v": 1}
        assert result2["payload"] == {"v": 2}
