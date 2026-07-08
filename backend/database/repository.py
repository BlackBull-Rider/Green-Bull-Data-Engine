"""
=========================================================
Green Bull Rider V6
Database Repository
=========================================================
Single Source of Truth for market.db
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from backend.database.connection import DatabaseConnection


class MarketRepository:

    def __init__(self, database_path: str | Path):

        self.db = DatabaseConnection(database_path)

    # --------------------------------------------------
    # Generic
    # --------------------------------------------------

    def fetch_one(
        self,
        query: str,
        params: tuple = (),
    ) -> sqlite3.Row | None:

        cursor = self.db.cursor()

        cursor.execute(query, params)

        return cursor.fetchone()

    def fetch_all(
        self,
        query: str,
        params: tuple = (),
    ) -> list[sqlite3.Row]:

        cursor = self.db.cursor()

        cursor.execute(query, params)

        return cursor.fetchall()

    def execute(
        self,
        query: str,
        params: tuple = (),
    ) -> None:

        cursor = self.db.cursor()

        cursor.execute(query, params)

        self.db.commit()

    # --------------------------------------------------
    # Historical Data
    # --------------------------------------------------

    def get_history(
        self,
        symbol: str,
        limit: int | None = None,
    ) -> list[sqlite3.Row]:

        sql = """
        SELECT *
        FROM historical_data
        WHERE symbol=?
        ORDER BY date ASC
        """

        if limit:

            sql += f" LIMIT {int(limit)}"

        return self.fetch_all(sql, (symbol.upper(),))

    # --------------------------------------------------
    # Latest Indicators
    # --------------------------------------------------

    def get_latest_indicators(
        self,
        symbol: str,
    ) -> sqlite3.Row | None:

        return self.fetch_one(
            """
            SELECT *
            FROM latest_indicators
            WHERE symbol=?
            """,
            (symbol.upper(),),
        )

    # --------------------------------------------------
    # Fundamental
    # --------------------------------------------------

    def get_fundamental(
        self,
        symbol: str,
    ) -> sqlite3.Row | None:

        return self.fetch_one(
            """
            SELECT *
            FROM fundamental_data
            WHERE symbol=?
            """,
            (symbol.upper(),),
        )

    # --------------------------------------------------
    # IPO
    # --------------------------------------------------

    def get_ipo(
        self,
        symbol: str,
    ) -> sqlite3.Row | None:

        return self.fetch_one(
            """
            SELECT *
            FROM ipo_data
            WHERE symbol=?
            """,
            (symbol.upper(),),
        )

    # --------------------------------------------------
    # Stock Master
    # --------------------------------------------------

    def get_stock(
        self,
        symbol: str,
    ) -> sqlite3.Row | None:

        return self.fetch_one(
            """
            SELECT *
            FROM stock_master
            WHERE symbol=?
            """,
            (symbol.upper(),),
        )

    # --------------------------------------------------
    # Dashboard Metrics
    # --------------------------------------------------

    def get_dashboard_metrics(self):

        return self.fetch_all(
            """
            SELECT *
            FROM dashboard_metrics
            """
        )

    # --------------------------------------------------
    # Market Signals
    # --------------------------------------------------

    def get_market_signals(self):

        return self.fetch_all(
            """
            SELECT *
            FROM market_signals
            """
        )

    # --------------------------------------------------
    # Update Log
    # --------------------------------------------------

    def get_update_log(self):

        return self.fetch_all(
            """
            SELECT *
            FROM update_log
            ORDER BY updated_at DESC
            """
        )

    # --------------------------------------------------
    # Exists
    # --------------------------------------------------

    def symbol_exists(
        self,
        symbol: str,
    ) -> bool:

        row = self.fetch_one(
            """
            SELECT symbol
            FROM stock_master
            WHERE symbol=?
            LIMIT 1
            """,
            (symbol.upper(),),
        )

        return row is not None

    # --------------------------------------------------
    # Count
    # --------------------------------------------------

    def count(
        self,
        table: str,
    ) -> int:

        row = self.fetch_one(
            f"SELECT COUNT(*) AS total FROM {table}"
        )

        return int(row["total"])

    # --------------------------------------------------
    # Raw Query
    # --------------------------------------------------

    def query(
        self,
        sql: str,
        params: tuple = (),
    ) -> list[sqlite3.Row]:

        return self.fetch_all(sql, params)
