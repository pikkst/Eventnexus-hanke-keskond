from __future__ import annotations

from typing import Any

from dramatiq.middleware import Middleware

from app.core.logging import get_logger

logger = get_logger()


class DeadLetterMiddleware(Middleware):
    def __init__(self, dead_letter_queue_name: str = "dead_letter", max_retries: int = 3) -> None:
        self.dead_letter_queue_name = dead_letter_queue_name
        self.max_retries = max_retries

    def after_process_message(self, broker: Any, message: Any, result: Any = None, exception: Any = None) -> None:
        if exception is not None:
            retries = message.options.get("retries", 0)
            if retries <= 0:
                logger.warning(
                    "Message moved to dead letter",
                    message_id=message.message_id,
                    actor_name=message.actor_name,
                    dead_letter_queue=self.dead_letter_queue_name,
                    error=str(exception),
                )
