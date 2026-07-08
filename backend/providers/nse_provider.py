"""
NEW AI BULL V1

NSE Provider

Primary Responsibility
----------------------
- Universe
- IPO
- Market Status

Python 3.13
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any

import pandas as pd
import requests

from backend.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class NSEProvider(BaseProvider):

    NSE_UNIVERSE_URL = (
        "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    )

    def __init__(self):

        self.session = requests.Session()

    # =====================================================
    # Universe
    # =====================================================

    def get_universe(self) -> pd.DataFrame:

        response = self.session.get(
            self.NSE_UNIVERSE_URL,
            timeout=30,
        )

        response.raise_for_status()

        df = pd.read_csv(
            self.NSE_UNIVERSE_URL
        )

        df = df.rename(
            columns={
                "SYMBOL": "symbol",
                "NAME OF COMPANY": "company_name",
            }
        )

        df = df[
            [
                "symbol",
                "company_name",
            ]
        ]

        df["exchange"] = "NSE"

        return df

    # =====================================================
    # BaseProvider Methods
    # =====================================================

    def get_history(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:

        return pd.DataFrame()

    def get_fundamentals(
        self,
        symbol: str,
    ) -> dict[str, Any]:

        return {}

    def get_financials(
        self,
        symbol: str,
    ) -> dict[str, Any]:

        return {}

    def get_listing_date(
        self,
        symbol: str,
    ) -> date | None:

        return None

    def is_available(self) -> bool:

        try:

            response = self.session.get(
                self.NSE_UNIVERSE_URL,
                timeout=10,
            )

            return response.status_code == 200

        except Exception:

            logger.exception(
                "NSE Provider unavailable."
            )

            return False

