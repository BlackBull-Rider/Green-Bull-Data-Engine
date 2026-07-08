"""
GREEN BULL DATA ENGINE
Analysis Schema
"""

from __future__ import annotations

import logging
import sqlite3

logger = logging.getLogger(__name__)


def create_analysis_tables(conn: sqlite3.Connection) -> None:
    """
    Creates analysis & dashboard related tables.
    Safe to run multiple times.
    """

    cursor = conn.cursor()

    # ==========================================================
    # DASHBOARD METRICS
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dashboard_metrics (

        date TEXT PRIMARY KEY,

        total_stocks INTEGER,

        long_term_buy INTEGER,
        swing_buy INTEGER,

        smart_money INTEGER,

        high_52w_count INTEGER,
        high_52w_breakout_count INTEGER,

        resistance_breakout_count INTEGER,
        support_breakdown_count INTEGER,

        pattern_breakout_count INTEGER,

        volume_explosion_count INTEGER,

        new_listing_count INTEGER,

        market_trend TEXT,

        top_bullish_stock TEXT,
        top_volume_stock TEXT,

        last_sync TEXT

    );
    """)

    # ==========================================================
    # MARKET SIGNALS
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_signals (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        symbol TEXT NOT NULL,

        signal_type TEXT NOT NULL,

        signal_score REAL,

        rank_no INTEGER,

        date TEXT

    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_market_signal_symbol
    ON market_signals(symbol);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_market_signal_date
    ON market_signals(date);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_market_signal_type
    ON market_signals(signal_type);
    """)

    # ==========================================================
    # IPO DATA
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ipo_data (

        symbol TEXT PRIMARY KEY,

        listing_date TEXT,

        listing_price REAL,
        current_price REAL,

        issue_size REAL,

        lot_size INTEGER,

        gmp REAL,

        promoter_holding REAL,
        institutional_holding REAL,

        market_cap REAL,

        volume_ratio REAL,

        below_listing INTEGER,

        updated_at TEXT

    );
    """)

    conn.commit()

    logger.info("Analysis schema initialized successfully.")

