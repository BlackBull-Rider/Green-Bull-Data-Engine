"""
GREEN BULL DATA ENGINE
Module: backend/automation/cleanup.py

Enterprise Cleanup Manager
Python 3.13 Compatible
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from backend.core.db import execute

logger = logging.getLogger(__name__)


class CleanupManager:

    def __init__(self) -> None:

        self.database_dir = Path("database")

        self.log_dir = Path("logs")

        self.cache_dir = Path(".cache")

    # ==========================================================
    # SQLITE
    # ==========================================================

    def optimize_database(self) -> None:

        logger.info("Running SQLite VACUUM...")

        execute("VACUUM")

        logger.info("Running SQLite ANALYZE...")

        execute("ANALYZE")

    # ==========================================================
    # CACHE
    # ==========================================================

    def cleanup_cache(self) -> None:

        if not self.cache_dir.exists():
            return

        removed = 0

        for item in self.cache_dir.rglob("*"):

            try:

                if item.is_file():

                    item.unlink()

                    removed += 1

            except Exception:

                logger.exception(
                    "Unable to delete cache file: %s",
                    item,
                )

        logger.info(
            "Cache cleaned (%d files).",
            removed,
        )

    # ==========================================================
    # PYTHON CACHE
    # ==========================================================

    def cleanup_pycache(self) -> None:

        removed = 0

        for directory in Path(".").rglob("__pycache__"):

            try:

                shutil.rmtree(directory)

                removed += 1

            except Exception:

                logger.exception(
                    "Unable to remove %s",
                    directory,
                )

        logger.info(
            "__pycache__ removed : %d",
            removed,
        )

    # ==========================================================
    # EMPTY LOGS
    # ==========================================================

    def cleanup_logs(self) -> None:

        if not self.log_dir.exists():
            return

        removed = 0

        for log in self.log_dir.glob("*.log"):

            try:

                if log.stat().st_size == 0:

                    log.unlink()

                    removed += 1

            except Exception:

                logger.exception(
                    "Unable to cleanup %s",
                    log,
                )

        logger.info(
            "Empty logs removed : %d",
            removed,
        )

    # ==========================================================
    # TEMP TABLES
    # ==========================================================

    def cleanup_retry_queue(self) -> None:

        from backend.core.db import table_exists

        if not table_exists("retry_queue"):
            logger.info("retry_queue table not found. Skipping.")
            return

        execute(
            """
            DELETE FROM retry_queue
            WHERE retry_count > 3
            """
        )

    # ==========================================================
    # MAIN
    # ==========================================================

    def run(self) -> None:

        logger.info("=" * 70)

        logger.info("GREEN BULL CLEANUP")

        logger.info("=" * 70)

        self.cleanup_cache()

        self.cleanup_pycache()

        self.cleanup_logs()

        self.cleanup_retry_queue()

        self.optimize_database()

        logger.info("=" * 70)

        logger.info("Cleanup Completed")

        logger.info("=" * 70)


cleanup = CleanupManager()


def run() -> None:

    cleanup.run()


if __name__ == "__main__":

    run()

