"""
GREEN BULL DATA ENGINE
Module: core/db.py

Enterprise SQLite Database Layer
Python 3.13 Compatible
"""

from __future__ import annotations

import logging
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

logger = logging.getLogger(__name__)

DATABASE_DIR = Path("database")
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATABASE_DIR / "market.db"


def get_connection() -> sqlite3.Connection:
    """
    Create an optimized SQLite connection.
    """

    conn = sqlite3.connect(
        DB_PATH,
        timeout=30,
    )

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute("PRAGMA busy_timeout=30000;")
    conn.execute("PRAGMA temp_store=MEMORY;")
    conn.execute("PRAGMA cache_size=-64000;")

    return conn


@contextmanager
def get_db() -> Iterator[sqlite3.Connection]:
    """
    Context managed database connection.

    Example:
        with get_db() as conn:
            ...
    """

    conn = get_connection()

    try:
        yield conn
        conn.commit()

    except Exception:
        conn.rollback()
        logger.exception("Database transaction rolled back.")
        raise

    finally:
        conn.close()


def execute(query: str, params: tuple = ()) -> None:
    """
    Execute a single SQL statement.
    """

    with get_db() as conn:
        conn.execute(query, params)


def executemany(query: str, rows) -> None:
    """
    Bulk insert/update helper.
    """

    with get_db() as conn:
        conn.executemany(query, rows)


def fetchone(query: str, params: tuple = ()):
    """
    Fetch one row.
    """

    with get_db() as conn:
        return conn.execute(query, params).fetchone()


def fetchall(query: str, params: tuple = ()):
    """
    Fetch all rows.
    """

    with get_db() as conn:
        return conn.execute(query, params).fetchall()


def table_exists(table_name: str) -> bool:
    """
    Check whether a table exists.
    """

    row = fetchone(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name=?
        """,
        (table_name,),
    )

    return row is not None


def database_health() -> bool:
    """
    Quick database integrity check.
    """

    try:
        row = fetchone("PRAGMA integrity_check;")
        return row[0] == "ok"

    except Exception:
        logger.exception("Database integrity check failed.")
        return False
