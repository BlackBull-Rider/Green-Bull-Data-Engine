"""
NEW AI BULL V1

Base Pipeline

All pipelines inherit from this class.

Python 3.13
"""

from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime

logger = logging.getLogger(__name__)


class BasePipeline(ABC):

    def __init__(self, name: str):

        self.name = name

        self.start_time = None

        self.end_time = None

    # =====================================================
    # Pipeline Life Cycle
    # =====================================================

    def execute(self):

        self.start()

        try:

            self.run()

            self.finish()

        except Exception:

            logger.exception(
                "%s Pipeline Failed",
                self.name,
            )

            self.rollback()

            raise

    # =====================================================

    def start(self):

        self.start_time = time.time()

        logger.info(
            "=" * 60
        )

        logger.info(
            "Starting %s Pipeline",
            self.name,
        )

    # =====================================================

    def finish(self):

        self.end_time = time.time()

        elapsed = self.end_time - self.start_time

        logger.info(
            "%s Pipeline Finished",
            self.name,
        )

        logger.info(
            "Execution Time : %.2f sec",
            elapsed,
        )

        logger.info(
            "=" * 60
        )

    # =====================================================

    def rollback(self):

        logger.warning(
            "%s Pipeline Rollback",
            self.name,
        )

    # =====================================================

    def log(self, message: str):

        logger.info(
            "[%s] %s",
            self.name,
            message,
        )

    # =====================================================

    def warning(self, message: str):

        logger.warning(
            "[%s] %s",
            self.name,
            message,
        )

    # =====================================================

    def error(self, message: str):

        logger.error(
            "[%s] %s",
            self.name,
            message,
        )

    # =====================================================

    @abstractmethod
    def run(self):

        """
        Main pipeline implementation.
        """

        raise NotImplementedError

