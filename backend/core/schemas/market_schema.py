"""
GREEN BULL DATA ENGINE
Market Schema
"""

from __future__ import annotations

import logging
import sqlite3

logger = logging.getLogger(__name__)


def create_market_tables(conn: sqlite3.Connection) -> None:
    """
    Creates market related tables.
    Safe to run multiple times.
    """

    cursor = conn.cursor()

    # ==========================================================
    # HISTORICAL DATA
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historical_data (

        symbol TEXT NOT NULL,

        date TEXT NOT NULL,

        open REAL,
        high REAL,
        low REAL,
        close REAL,

        volume REAL,

        PRIMARY KEY (
            symbol,
            date
        )

    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_history_symbol
    ON historical_data(symbol);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_history_date
    ON historical_data(date);
    """)

    # ==========================================================
    # CORPORATE ACTIONS
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS corporate_actions (

        symbol TEXT NOT NULL,

        action_date TEXT NOT NULL,

        action_type TEXT NOT NULL,

        dividend REAL,

        split_ratio REAL,

        bonus_ratio REAL,

        rights_ratio REAL,

        face_value_change REAL,

        buyback REAL,

        merger REAL,

        demerger REAL,

        spin_off REAL,

        description TEXT,

        updated_at TEXT,

        PRIMARY KEY (
            symbol,
            action_date,
            action_type
        )

    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_actions_symbol
    ON corporate_actions(symbol);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_actions_date
    ON corporate_actions(action_date);
    """)

    conn.commit()

    logger.info("Market schema initialized successfully.")
