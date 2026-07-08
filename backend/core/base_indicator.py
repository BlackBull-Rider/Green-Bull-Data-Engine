"""
=========================================================
Green Bull Rider V6
Base Indicator Class
=========================================================
All indicators inherit from this class.
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy as np


class BaseIndicator(ABC):
    """
    Base class for all technical indicators.
    """

    def __init__(self, period: int):

        if period <= 0:
            raise ValueError("period must be greater than zero")

        self.period = int(period)

    # ----------------------------------------------------

    @staticmethod
    def as_array(data: Any) -> np.ndarray:

        arr = np.asarray(data, dtype=np.float64)

        if arr.ndim != 1:
            raise ValueError("Input must be one-dimensional")

        return arr

    # ----------------------------------------------------

    @staticmethod
    def empty(length: int):

        return np.full(length, np.nan, dtype=np.float64)

    # ----------------------------------------------------

    @staticmethod
    def validate_length(data, period):

        if len(data) < period:
            raise ValueError(
                f"Need at least {period} values."
            )

    # ----------------------------------------------------

    @property
    def name(self):

        return self.__class__.__name__

    # ----------------------------------------------------

    @abstractmethod
    def calculate(self, *args, **kwargs):

        """
        Calculate indicator.
        """
        raise NotImplementedError
