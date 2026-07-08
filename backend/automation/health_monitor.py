"""
GREEN BULL DATA ENGINE
Module: backend/automation/health_monitor.py

Enterprise Health Monitor
Python 3.13 Compatible
"""

from __future__ import annotations

import logging
from datetime import datetime

from backend.core.db import database_health, fetchone
from backend.providers.yahoo_provider import YahooProvider
from backend.automation.retry_manager import retry_manager

logger = logging.getLogger(__name__)


class HealthMonitor:

    def __init__(self) -> None:

        self.provider = YahooProvider()

    # =====================================================
    # DATABASE
    # =====================================================

    def database(self) -> bool:

        ok = database_health()

        logger.info(
            "Database Health : %s",
            "OK" if ok else "FAILED",
        )

        return ok

    # =====================================================
    # PROVIDER
    # =====================================================

    def provider_status(self) -> bool:

        try:

            ok = self.provider.is_available()

        except Exception:

            ok = False

        logger.info(
            "Yahoo Provider  : %s",
            "ONLINE" if ok else "OFFLINE",
        )

        return ok

    # =====================================================
    # LAST UPDATE
    # =====================================================

    def last_pipeline(self):

        row = fetchone(
            """
            SELECT
                last_run,
                status
            FROM update_log
            WHERE process_name='DATA_PIPELINE'
            """
        )

        if row:

            logger.info(
                "Last Pipeline  : %s",
                row["last_run"],
            )

            logger.info(
                "Pipeline Status: %s",
                row["status"],
            )

        else:

            logger.warning(
                "Pipeline has never been executed."
            )

    # =====================================================
    # RETRY QUEUE
    # =====================================================

    def retry_queue(self):

        retry_manager.load()

        logger.info(
            "Retry Queue    : %d",
            retry_manager.size(),
        )

    # =====================================================
    # DATABASE SIZE
    # =====================================================

    def coverage(self):

        tables = [

            "historical_data",
            "fundamental_data",
            "financial_data",
            "company_profile",
            "corporate_actions",
            "shareholding_data",
            "analyst_data",
            "earnings_history",

        ]

        logger.info("-" * 60)

        for table in tables:

            try:

                row = fetchone(
                    f"SELECT COUNT(*) FROM {table}"
                )

                logger.info(
                    "%-22s %8d",
                    table,
                    row[0],
                )

            except Exception:

                logger.warning(
                    "%s unavailable.",
                    table,
                )

    # =====================================================
    # REPORT
    # =====================================================

    def run(self):

        logger.info("=" * 70)
        logger.info("GREEN BULL HEALTH REPORT")
        logger.info(
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
        logger.info("=" * 70)

        self.database()

        self.provider_status()

        self.last_pipeline()

        self.retry_queue()

        self.coverage()

        logger.info("=" * 70)


health_monitor = HealthMonitor()


def run():

    health_monitor.run()


if __name__ == "__main__":

    run()

