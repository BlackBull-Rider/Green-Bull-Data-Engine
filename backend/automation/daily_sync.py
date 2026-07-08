"""
GREEN BULL DATA ENGINE
Module: backend/automation/daily_sync.py

Daily Synchronization Job

Python 3.13 Compatible
"""

from __future__ import annotations

import logging
import time
from datetime import datetime

from backend.pipeline.data_pipeline import DataPipeline
from backend.core.db import execute

logger = logging.getLogger(__name__)


class DailySync:

    JOB_NAME = "DAILY_SYNC"

    def __init__(self):

        self.pipeline = DataPipeline()

    def _job_started(self):

        execute(
            """
            INSERT OR REPLACE INTO update_log
            (
                process_name,
                last_run,
                status
            )
            VALUES
            (
                ?,
                ?,
                ?
            )
            """,
            (
                self.JOB_NAME,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "RUNNING",
            ),
        )

    def _job_finished(
        self,
        elapsed: float,
    ):

        execute(
            """
            INSERT OR REPLACE INTO update_log
            (
                process_name,
                last_run,
                status
            )
            VALUES
            (
                ?,
                ?,
                ?
            )
            """,
            (
                self.JOB_NAME,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                f"SUCCESS ({elapsed:.2f}s)",
            ),
        )

    def _job_failed(
        self,
        error: Exception,
    ):

        execute(
            """
            INSERT OR REPLACE INTO update_log
            (
                process_name,
                last_run,
                status
            )
            VALUES
            (
                ?,
                ?,
                ?
            )
            """,
            (
                self.JOB_NAME,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                f"FAILED : {error}",
            ),
        )

    def run(self):

        logger.info("=" * 70)
        logger.info("DAILY MARKET SYNCHRONIZATION")
        logger.info("=" * 70)

        started = time.perf_counter()

        try:

            self._job_started()

            self.pipeline.execute()

            elapsed = time.perf_counter() - started

            self._job_finished(elapsed)

            logger.info(
                "Daily Sync Completed (%.2fs)",
                elapsed,
            )

        except Exception as exc:

            self._job_failed(exc)

            logger.exception(
                "Daily Sync Failed"
            )

            raise


daily_sync = DailySync()


def run():

    daily_sync.run()


if __name__ == "__main__":

    run()

