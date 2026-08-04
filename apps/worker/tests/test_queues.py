from __future__ import annotations

from app.config import QueueName


class TestQueueConstants:
    def test_default_queue_constant(self) -> None:
        assert QueueName.DEFAULT is QueueName.DEFAULT

    def test_high_queue_constant(self) -> None:
        assert QueueName.HIGH is QueueName.HIGH

    def test_low_queue_constant(self) -> None:
        assert QueueName.LOW is QueueName.LOW

    def test_dead_letter_queue_constant(self) -> None:
        assert QueueName.DEAD_LETTER is QueueName.DEAD_LETTER
