"""
GREEN BULL DATA ENGINE
Indicator Schema
"""

from __future__ import annotations

import logging
import sqlite3

logger = logging.getLogger(__name__)


def create_indicator_tables(conn: sqlite3.Connection) -> None:
    """
    Creates indicator tables.
    Safe to run multiple times.
    """

    cursor = conn.cursor()

    # ==========================================================
    # INDICATORS
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS indicators (

        symbol TEXT NOT NULL,
        date TEXT NOT NULL,

        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL,

        ema20 REAL,
        ema50 REAL,
        ema200 REAL,

        sma20 REAL,
        sma50 REAL,
        sma200 REAL,

        rsi REAL,

        macd REAL,
        macd_signal REAL,
        macd_hist REAL,

        atr REAL,

        adx REAL,
        plus_di REAL,
        minus_di REAL,

        bb_upper REAL,
        bb_middle REAL,
        bb_lower REAL,

        stochastic_k REAL,
        stochastic_d REAL,

        cci REAL,
        williams_r REAL,

        obv REAL,
        vwap REAL,

        volume_avg20 REAL,

        breakout_score REAL,
        swing_score REAL,

        supertrend REAL,
        trend TEXT,

        pivot REAL,
        cpr_top REAL,
        cpr_bottom REAL,

        r1 REAL,
        r2 REAL,
        r3 REAL,

        s1 REAL,
        s2 REAL,
        s3 REAL,

        PRIMARY KEY (
            symbol,
            date
        )

    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_indicators_symbol
    ON indicators(symbol);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_indicators_date
    ON indicators(date);
    """)

    # ==========================================================
    # LATEST INDICATORS
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS latest_indicators (

        symbol TEXT PRIMARY KEY,

        date TEXT,

        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL,

        ema20 REAL,
        ema50 REAL,
        ema200 REAL,

        sma20 REAL,
        sma50 REAL,
        sma200 REAL,

        rsi REAL,

        macd REAL,
        macd_signal REAL,
        macd_hist REAL,

        atr REAL,

        adx REAL,
        plus_di REAL,
        minus_di REAL,

        bb_upper REAL,
        bb_middle REAL,
        bb_lower REAL,

        stochastic_k REAL,
        stochastic_d REAL,

        cci REAL,
        williams_r REAL,

        obv REAL,
        vwap REAL,

        volume_avg20 REAL,

        breakout_score REAL,
        swing_score REAL,

        supertrend REAL,
        trend TEXT,

        pivot REAL,
        cpr_top REAL,
        cpr_bottom REAL,

        r1 REAL,
        r2 REAL,
        r3 REAL,

        s1 REAL,
        s2 REAL,
        s3 REAL

    );
    """)

    conn.commit()

    logger.info("Indicator schema initialized successfully.")

