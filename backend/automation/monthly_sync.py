"""
GREEN BULL DATA ENGINE
Module: backend/automation/monthly_sync.py

Monthly Synchronization Job

Python 3.13 Compatible
"""

from __future__ import annotations

import logging
import time
from datetime import datetime

from backend.core.db import execute, fetchone

logger = logging.getLogger(__name__)


class MonthlySync:

    JOB_NAME = "MONTHLY_SYNC"

    def _update_status(self, status: str) -> None:

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
                ?, ?, ?
            )
            """,
            (
                self.JOB_NAME,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status,
            ),
        )

    def validate_database(self) -> None:

        logger.info("Running SQLite Integrity Check...")

        result = fetchone("PRAGMA integrity_check")

        if result and result[0] != "ok":
            raise RuntimeError("Database integrity check failed.")

    def analyze_tables(self) -> None:

        logger.info("Analyzing database statistics...")

        execute("ANALYZE")

    def optimize_database(self) -> None:

        logger.info("Optimizing database...")

        execute("VACUUM")

    def rebuild_indexes(self) -> None:

        logger.info("Rebuilding indexes...")

        # Future Index Maintenance

    def coverage_report(self) -> None:

        logger.info("Generating coverage report...")

        tables = [
            "historical_data",
            "fundamental_data",
            "financial_data",
            "company_profile",
            "corporate_actions",
            "shareholding_data",
            "analyst_data",
            "earnings_history",
            "latest_indicators",
            "dashboard_metrics",
        ]

        for table in tables:

            try:

                row = fetchone(
                    f"SELECT COUNT(*) FROM {table}"
                )

                logger.info(
                    "%-25s : %s",
                    table,
                    row[0],
                )

            except Exception:

                logger.warning(
                    "%s not available.",
                    table,
                )

    def run(self) -> None:

        logger.info("=" * 70)
        logger.info("MONTHLY DATABASE MAINTENANCE")
        logger.info("=" * 70)

        started = time.perf_counter()

        try:

            self._update_status("RUNNING")

            self.validate_database()

            self.analyze_tables()

            self.optimize_database()

            self.rebuild_indexes()

            self.coverage_report()

            elapsed = time.perf_counter() - started

            self._update_status(
                f"SUCCESS ({elapsed:.2f}s)"
            )

            logger.info(
                "Monthly Sync Completed (%.2fs)",
                elapsed,
            )

        except Exception as exc:

            self._update_status(
                f"FAILED : {exc}"
            )

            logger.exception(
                "Monthly Sync Failed"
            )

            raise


monthly_sync = MonthlySync()


def run() -> None:

    monthly_sync.run()


if __name__ == "__main__":

    run()

