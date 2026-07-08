"""
GREEN BULL DATA ENGINE
Module: backend/automation/scheduler.py

Enterprise Automation Scheduler
Python 3.13 Compatible
"""

from __future__ import annotations

import logging
import time
from datetime import datetime
from typing import Callable

from backend.automation.job_registry import enabled_jobs

logger = logging.getLogger(__name__)


class Scheduler:

    def __init__(self) -> None:

        self.running = False

    def _run_job(self, job) -> None:

        if job.runner is None:
            logger.warning(
                "%s has no runner attached.",
                job.name,
            )
            return

        logger.info("=" * 70)
        logger.info("Starting Job : %s", job.name)

        started = time.perf_counter()

        try:

            job.runner()

            elapsed = time.perf_counter() - started

            logger.info(
                "Completed : %s (%.2fs)",
                job.name,
                elapsed,
            )

        except Exception:

            logger.exception(
                "Automation job failed : %s",
                job.name,
            )

    def run_once(self) -> None:
        """
        Execute every enabled job one time.
        """

        for _, job in enabled_jobs().items():
            self._run_job(job)

    def run_forever(
        self,
        interval_seconds: int = 60,
    ) -> None:
        """
        Lightweight scheduler loop.
        """

        self.running = True

        logger.info("=" * 70)
        logger.info("Automation Scheduler Started")
        logger.info("=" * 70)

        while self.running:

            now = datetime.now()

            logger.info(
                "Scheduler Tick : %s",
                now.strftime("%Y-%m-%d %H:%M:%S"),
            )

            self.run_once()

            time.sleep(interval_seconds)

    def stop(self) -> None:

        self.running = False

        logger.info("Automation Scheduler Stopped")


scheduler = Scheduler()


if __name__ == "__main__":

    scheduler.run_once()

