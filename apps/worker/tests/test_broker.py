from __future__ import annotations

from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware import AgeLimit, TimeLimit

from app.config import AppEnvironment, Settings
from app.core.middleware import DeadLetterMiddleware
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
        "worker_task_timeout": 30000,
        "worker_max_retries": 5,
        "worker_retry_delay": 2000,
        "worker_dead_letter_queue": "dead_letter",
        "worker_health_port": 8001,
        "log_level": "DEBUG",
        "log_format": "console",
    }
    defaults.update(overrides)
    return Settings(**defaults)  # type: ignore[arg-type]


class TestBrokerConfiguration:
    def test_broker_has_dead_letter_middleware(self) -> None:
        settings = _make_test_settings()
        broker = _create_broker(settings)
        assert isinstance(broker, RedisBroker)
        middleware_types = [type(m) for m in broker.middleware]
        assert DeadLetterMiddleware in middleware_types

    def test_broker_has_max_retries_with_correct_count(self) -> None:
        settings = _make_test_settings(worker_max_retries=5)
        broker = _create_broker(settings)
        middleware_types = [type(m) for m in broker.middleware]
        assert DeadLetterMiddleware in middleware_types
        mw = next(m for m in broker.middleware if isinstance(m, DeadLetterMiddleware))
        assert mw.max_retries == 5

    def test_broker_has_time_limit_with_correct_value(self) -> None:
        settings = _make_test_settings(worker_task_timeout=45000)
        broker = _create_broker(settings)
        middleware_types = [type(m) for m in broker.middleware]
        assert TimeLimit in middleware_types
        time_limit_mw = next(m for m in broker.middleware if isinstance(m, TimeLimit))
        assert time_limit_mw.time_limit == 45000

    def test_broker_has_age_limit_middleware(self) -> None:
        settings = _make_test_settings()
        broker = _create_broker(settings)
        middleware_types = [type(m) for m in broker.middleware]
        assert AgeLimit in middleware_types
