"""
=========================================================
Green Bull Rider V6
Base Brain
=========================================================
"""

from abc import ABC, abstractmethod


class BaseBrain(ABC):

    @abstractmethod
    def process(self, payload: dict) -> dict:
        """
        Merge engine outputs into unified payload.
        """
        raise NotImplementedError
