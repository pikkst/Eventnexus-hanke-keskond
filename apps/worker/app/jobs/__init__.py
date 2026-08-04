from __future__ import annotations

import json
import time
from typing import Any, cast

from pydantic import BaseModel, Field

from app.core.logging import get_logger

logger = get_logger()

_idempotency_store: dict[str, tuple[str, float]] = {}
_idempotency_ttl: int = 86400


class SampleJobResult(BaseModel):
    job_id: str
    idempotency_key: str
    status: str
    processed_at: float
    payload: dict[str, Any]


class IdempotentJobPayload(BaseModel):
    idempotency_key: str = Field(..., min_length=1, description="Unique idempotency key")
    payload: dict[str, Any] = Field(default_factory=dict, description="Arbitrary job payload")
    simulate_failure: bool = Field(default=False, description="Simulate a processing failure")


def _cleanup_expired() -> None:
    now = time.time()
    expired = [k for k, (_, ts) in _idempotency_store.items() if now - ts > _idempotency_ttl]
    for key in expired:
        del _idempotency_store[key]


def run_sample_job(
    idempotency_key: str,
    payload: dict[str, Any] | None = None,
    simulate_failure: bool = False,
    job_id: str | None = None,
) -> dict[str, Any]:
    _cleanup_expired()

    if idempotency_key in _idempotency_store:
        result_str, _ = _idempotency_store[idempotency_key]
        logger.info(
            "Duplicate job handled safely",
            idempotency_key=idempotency_key,
            result=cast(dict[str, Any], json.loads(result_str)),
        )
        return cast(dict[str, Any], json.loads(result_str))

    if simulate_failure:
        logger.error("Simulated job failure", idempotency_key=idempotency_key)
        raise RuntimeError("Simulated processing failure")

    result = SampleJobResult(
        job_id=job_id or __import__("uuid").uuid4().hex,
        idempotency_key=idempotency_key,
        status="processed",
        processed_at=time.time(),
        payload=payload or {},
    )
    result_dict = result.model_dump()
    _idempotency_store[idempotency_key] = (json.dumps(result_dict), time.time())

    logger.info(
        "Sample job processed",
        idempotency_key=idempotency_key,
        job_id=result.job_id,
    )
    return result_dict
