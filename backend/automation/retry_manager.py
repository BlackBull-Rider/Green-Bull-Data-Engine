"""
GREEN BULL DATA ENGINE
Module: backend/automation/retry_manager.py

Retry Manager

Python 3.13 Compatible
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Dict, List

from backend.core.db import execute, fetchall

logger = logging.getLogger(__name__)


class RetryManager:

    MAX_RETRIES = 3

    def __init__(self):

        self.queue: Dict[str, int] = {}

    # ==========================================================
    # Queue
    # ==========================================================

    def add(self, symbol: str) -> None:

        self.queue[symbol] = self.queue.get(symbol, 0) + 1

        logger.warning(
            "Queued %s (Retry %d)",
            symbol,
            self.queue[symbol],
        )

    def remove(self, symbol: str) -> None:

        self.queue.pop(symbol, None)

    def clear(self) -> None:

        self.queue.clear()

    def size(self) -> int:

        return len(self.queue)

    # ==========================================================
    # Status
    # ==========================================================

    def failed_symbols(self) -> List[str]:

        return [
            s
            for s, r in self.queue.items()
            if r <= self.MAX_RETRIES
        ]

    def exhausted_symbols(self) -> List[str]:

        return [
            s
            for s, r in self.queue.items()
            if r > self.MAX_RETRIES
        ]

    # ==========================================================
    # Database
    # ==========================================================

    def save(self) -> None:

        execute(
            """
            CREATE TABLE IF NOT EXISTS retry_queue (

                symbol TEXT PRIMARY KEY,

                retry_count INTEGER,

                updated_at TEXT

            )
            """
        )

        execute("DELETE FROM retry_queue")

        rows = [
            (
                symbol,
                retry,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            )
            for symbol, retry in self.queue.items()
        ]

        if rows:

            from backend.core.db import executemany

            executemany(
                """
                INSERT INTO retry_queue
                VALUES (?, ?, ?)
                """,
                rows,
            )

    def load(self) -> None:

        try:

            rows = fetchall(
                """
                SELECT
                    symbol,
                    retry_count
                FROM retry_queue
                """
            )

        except Exception:

            return

        self.queue = {
            row["symbol"]: row["retry_count"]
            for row in rows
        }

    # ==========================================================
    # Report
    # ==========================================================

    def summary(self) -> None:

        logger.info("=" * 60)

        logger.info(
            "Retry Queue : %d",
            self.size(),
        )

        logger.info(
            "Retryable   : %d",
            len(self.failed_symbols()),
        )

        logger.info(
            "Exhausted   : %d",
            len(self.exhausted_symbols()),
        )

        logger.info("=" * 60)


retry_manager = RetryManager()


if __name__ == "__main__":

    retry_manager.load()

    retry_manager.summary()

