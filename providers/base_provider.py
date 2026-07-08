"""
GREEN BULL DATA ENGINE

Module: providers/base_provider.py

Base Provider Interface
Python 3.13
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import Any

import pandas as pd


class BaseProvider(ABC):
    """
    Base interface for all market data providers.
    """

    @abstractmethod
    def get_history(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> pd.DataFrame:
        """
        Return historical OHLCV data.
        """
        raise NotImplementedError

    @abstractmethod
    def get_fundamentals(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """
        Return company fundamentals.
        """
        raise NotImplementedError

    @abstractmethod
    def get_financials(
        self,
        symbol: str,
    ) -> dict[str, Any]:
        """
        Return financial statements.
        """
        raise NotImplementedError

    @abstractmethod
    def get_listing_date(
        self,
        symbol: str,
    ) -> date | None:
        """
        Return company listing date.
        """
        raise NotImplementedError

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check provider availability.
        """
        raise NotImplementedError
