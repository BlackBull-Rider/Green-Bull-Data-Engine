"""
=========================================================
Green Bull Rider V6
Base Engine
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseEngine(ABC):

    def __init__(self, repository):

        self.repository = repository

    @property
    def name(self):

        return self.__class__.__name__

    @abstractmethod
    def analyze(self, symbol: str) -> dict[str, Any]:
        """
        Must return JSON Observation.
        """
        raise NotImplementedError
