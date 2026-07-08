"""
GREEN BULL DATA ENGINE
Database Schema Entry Point

This module is the only public entry point for creating
or initializing the complete database schema.
"""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path
from typing import Optional

from backend.core.schemas.master_schema import create_all_tables

logger = logging.getLogger(__name__)


DEFAULT_DB_PATH = Path("database/market.db")


def initialize_database(
    db_path: Optional[str | Path] = None,
) -> None:
    """
    Initialize complete database schema.

    Safe to call multiple times.
    """

    database = Path(db_path) if db_path else DEFAULT_DB_PATH

    database.parent.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 80)
    logger.info("Initializing Green Bull Database...")
    logger.info(f"Database : {database}")
    logger.info("=" * 80)

    conn = sqlite3.connect(str(database))

    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        conn.execute("PRAGMA temp_store=MEMORY;")

        create_all_tables(conn)

        conn.commit()

        logger.info("=" * 80)
        logger.info("Database initialization completed successfully.")
        logger.info("=" * 80)

    except Exception:
        conn.rollback()
        logger.exception("Database initialization failed.")
        raise

    finally:
        conn.close()


def recreate_database(
    db_path: Optional[str | Path] = None,
) -> None:
    """
    Drop database file and recreate every table.
    """

    database = Path(db_path) if db_path else DEFAULT_DB_PATH

    if database.exists():
        database.unlink()

    initialize_database(database)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    initialize_database()

