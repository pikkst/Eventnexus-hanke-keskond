from __future__ import annotations

from enum import StrEnum


class QueueName(StrEnum):
    DEFAULT = "default"
    HIGH = "high"
    LOW = "low"
    DEAD_LETTER = "dead_letter"
