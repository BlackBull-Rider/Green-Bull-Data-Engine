"""
=========================================================
Green Bull Rider V6
Base Repository
=========================================================
"""

from abc import ABC, abstractmethod


class BaseRepository(ABC):

    @abstractmethod
    def fetch_one(self, query, params=()):
        raise NotImplementedError

    @abstractmethod
    def fetch_all(self, query, params=()):
        raise NotImplementedError

    @abstractmethod
    def execute(self, query, params=()):
        raise NotImplementedError
