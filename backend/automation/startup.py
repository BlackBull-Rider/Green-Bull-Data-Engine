"""
GREEN BULL DATA ENGINE
Master Automation Service

Python 3.13
"""

from __future__ import annotations

import logging
import signal
import sys
import time

from datetime import datetime

from backend.automation.daily_sync import run as daily_sync
from backend.automation.weekly_sync import run as weekly_sync
from backend.automation.monthly_sync import run as monthly_sync
from backend.automation.health_monitor import run as health_monitor
from backend.automation.cleanup import run as cleanup


logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s"

)

logger = logging.getLogger("Automation")


class AutomationService:

    def __init__(self):

        self.running = True

        self.last_daily = None

        self.last_weekly = None

        self.last_monthly = None

        self.last_health = None

        signal.signal(
            signal.SIGINT,
            self.shutdown
        )

        signal.signal(
            signal.SIGTERM,
            self.shutdown
        )

    def shutdown(
        self,
        *_,
    ):

        logger.info("Automation stopping...")

        self.running = False

    def market_closed(
        self,
    ) -> bool:

        now = datetime.now()

        if now.weekday() >= 5:
            return False

        if now.hour > 15:
            return True

        if now.hour == 15 and now.minute >= 35:
            return True

        return False

    def daily_job(self):

        today = datetime.now().date()

        if self.last_daily == today:
            return

        logger.info("=" * 70)

        logger.info("DAILY JOB")

        logger.info("=" * 70)

        daily_sync()

        self.last_daily = today

    def weekly_job(self):

        now = datetime.now()

        if now.weekday() != 6:
            return

        today = now.date()

        if self.last_weekly == today:
            return

        logger.info("=" * 70)

        logger.info("WEEKLY JOB")

        logger.info("=" * 70)

        weekly_sync()

        self.last_weekly = today


    def monthly_job(self):

        now = datetime.now()

        if now.day != 1:
            return

        today = now.date()

        if self.last_monthly == today:
            return

        logger.info("=" * 70)
        logger.info("MONTHLY JOB")
        logger.info("=" * 70)

        monthly_sync()

        self.last_monthly = today

    def heartbeat(self):

        now = datetime.now()

        if (
            self.last_health is not None
            and (now - self.last_health).total_seconds() < 1800
        ):
            return

        self.last_health = now

        logger.info(
            "Heartbeat | %s",
            now.strftime("%Y-%m-%d %H:%M:%S"),
        )

        try:
            health_monitor()
        except Exception:
            logger.exception("Health monitor failed.")

    def maintenance(self):

        try:
            cleanup()
        except Exception:
            logger.exception("Cleanup failed.")

    def run(self):

        logger.info("=" * 70)
        logger.info("GREEN BULL MASTER AUTOMATION STARTED")
        logger.info("=" * 70)

        while self.running:

            try:

                self.heartbeat()

                if self.market_closed():

                    self.daily_job()

                self.weekly_job()

                self.monthly_job()

                if datetime.now().weekday() == 6:
                    self.maintenance()

                logger.info("Sleeping for 60 seconds...")
                time.sleep(60)

            except Exception:

                logger.exception(
                    "Automation loop crashed. Recovering in 60 seconds..."
                )

                time.sleep(60)


service = AutomationService()


def main():

    service.run()


if __name__ == "__main__":

    main()

