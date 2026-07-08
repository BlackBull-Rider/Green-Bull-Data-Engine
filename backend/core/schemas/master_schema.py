"""
GREEN BULL DATA ENGINE
Master Schema Manager

Creates every database table in the correct order.
"""

from __future__ import annotations

import logging
import sqlite3

from .stock_schema import create_stock_tables
from .market_schema import create_market_tables
from .fundamental_schema import create_fundamental_tables
from .indicator_schema import create_indicator_tables
from .analysis_schema import create_analysis_tables
from .system_schema import create_system_tables

logger = logging.getLogger(__name__)


def create_all_tables(conn: sqlite3.Connection) -> None:
    """
    Create every table required by Green Bull Data Engine.

    Safe to execute multiple times.
    """

    logger.info("=" * 70)
    logger.info("Initializing Green Bull Database Schema...")
    logger.info("=" * 70)

    create_stock_tables(conn)
    logger.info("✓ Stock Schema Ready")

    create_market_tables(conn)
    logger.info("✓ Market Schema Ready")

    create_fundamental_tables(conn)
    logger.info("✓ Fundamental Schema Ready")

    create_indicator_tables(conn)
    logger.info("✓ Indicator Schema Ready")

    create_analysis_tables(conn)
    logger.info("✓ Analysis Schema Ready")

    create_system_tables(conn)
    logger.info("✓ System Schema Ready")

    conn.commit()

    logger.info("=" * 70)
    logger.info("Green Bull Database Initialized Successfully.")
    logger.info("=" * 70)

