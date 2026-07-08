"""
=========================================================
Green Bull Rider V6
Base AI
=========================================================
"""

from abc import ABC, abstractmethod


class BaseAI(ABC):

    @abstractmethod
    def generate(self, payload: dict) -> dict:
        """
        Final AI decision layer.
        """
        raise NotImplementedError
