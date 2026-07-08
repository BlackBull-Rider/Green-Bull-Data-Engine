"""
GREEN BULL DATA ENGINE
Stock Schema
"""

from __future__ import annotations

import logging
import sqlite3

logger = logging.getLogger(__name__)


def create_stock_tables(conn: sqlite3.Connection) -> None:
    """
    Creates stock related tables.
    Safe to run multiple times.
    """

    cursor = conn.cursor()

    # ==========================================================
    # STOCK MASTER
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_master (

        symbol TEXT PRIMARY KEY,

        company_name TEXT,

        exchange TEXT,

        status TEXT DEFAULT 'ACTIVE',

        updated_at TEXT

    );
    """)

    # ==========================================================
    # COMPANY PROFILE
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS company_profile (

        symbol TEXT PRIMARY KEY,

        company_name TEXT,
        short_name TEXT,
        long_name TEXT,

        exchange TEXT,
        exchange_code TEXT,

        isin TEXT,

        sector TEXT,
        industry TEXT,
        sub_industry TEXT,

        market TEXT,

        currency TEXT,

        country TEXT,
        state TEXT,
        city TEXT,
        address TEXT,
        zipcode TEXT,

        website TEXT,
        phone TEXT,
        email TEXT,

        ceo TEXT,
        cfo TEXT,
        chairman TEXT,

        employees INTEGER,

        founded_year INTEGER,

        business_summary TEXT,

        logo_url TEXT,

        timezone TEXT,

        updated_at TEXT

    );
    """)

    conn.commit()

    logger.info("Stock schema initialized successfully.")
