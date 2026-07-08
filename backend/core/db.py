"""
GREEN BULL DATA ENGINE
Module: backend/core/db.py

Enterprise Database Layer
Python 3.13 Compatible
"""

from __future__ import annotations

import logging
import sqlite3
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Optional

import pandas as pd

from backend.core.schema import initialize_database

logger = logging.getLogger(__name__)

# ==========================================================
# PATHS
# ==========================================================

DATABASE_DIR = Path("database")
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATABASE_DIR / "market.db"

# ==========================================================
# CONFIGURATION
# ==========================================================

DEFAULT_TIMEOUT = 30
DEFAULT_BUSY_TIMEOUT = 30000
MAX_RETRIES = 5
RETRY_DELAY = 0.25

# ==========================================================
# THREAD LOCAL CONNECTION
# ==========================================================

_local = threading.local()


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

if not DB_PATH.exists():
    logger.info("Database not found. Initializing...")
    initialize_database(DB_PATH)


# ==========================================================
# CONNECTION FACTORY
# ==========================================================

def _create_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(
        DB_PATH,
        timeout=DEFAULT_TIMEOUT,
        check_same_thread=False,
    )

    conn.row_factory = sqlite3.Row

    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.execute(f"PRAGMA busy_timeout={DEFAULT_BUSY_TIMEOUT};")
    conn.execute("PRAGMA temp_store=MEMORY;")
    conn.execute("PRAGMA cache_size=-64000;")

    return conn


def get_connection() -> sqlite3.Connection:
    """
    Returns one connection per thread.
    """

    conn = getattr(_local, "connection", None)

    if conn is None:

        conn = _create_connection()

        _local.connection = conn

    return conn


def close_connection() -> None:
    """
    Close current thread connection.
    """

    conn = getattr(_local, "connection", None)

    if conn is None:
        return

    try:
        conn.close()
    finally:
        _local.connection = None


# ==========================================================
# RETRY EXECUTOR
# ==========================================================

def _execute_with_retry(func, *args, **kwargs):

    last_error = None

    for attempt in range(MAX_RETRIES):

        try:

            return func(*args, **kwargs)

        except sqlite3.OperationalError as exc:

            last_error = exc

            if "locked" not in str(exc).lower():
                raise

            logger.warning(
                "Database locked. Retry %d/%d",
                attempt + 1,
                MAX_RETRIES,
            )

            time.sleep(RETRY_DELAY)

    raise last_error


# ==========================================================
# CONTEXT MANAGER
# ==========================================================

@contextmanager
def get_db() -> Iterator[sqlite3.Connection]:

    conn = get_connection()

    try:

        yield conn

        conn.commit()

    except Exception:

        conn.rollback()

        logger.exception("Database transaction rolled back.")

        raise


# ==========================================================
# TRANSACTION
# ==========================================================

@contextmanager
def transaction() -> Iterator[sqlite3.Connection]:

    conn = get_connection()

    try:

        conn.execute("BEGIN")

        yield conn

        conn.commit()

    except Exception:

        conn.rollback()

        logger.exception("Transaction rolled back.")

        raise


# ==========================================================
# QUERY HELPERS
# ==========================================================

def execute(query: str, params: tuple = ()) -> None:
    """
    Execute a single SQL statement.
    """

    with get_db() as conn:

        _execute_with_retry(
            conn.execute,
            query,
            params,
        )


def executemany(query: str, rows) -> None:
    """
    Execute bulk SQL.
    """

    with get_db() as conn:

        _execute_with_retry(
            conn.executemany,
            query,
            rows,
        )


def fetchone(
    query: str,
    params: tuple = (),
):

    with get_db() as conn:

        cursor = _execute_with_retry(
            conn.execute,
            query,
            params,
        )

        return cursor.fetchone()


def fetchall(
    query: str,
    params: tuple = (),
):

    with get_db() as conn:

        cursor = _execute_with_retry(
            conn.execute,
            query,
            params,
        )

        return cursor.fetchall()


def execute_scalar(
    query: str,
    params: tuple = (),
) -> Any:
    """
    Return first column of first row.
    """

    row = fetchone(query, params)

    if row is None:
        return None

    return row[0]


def fetch_dataframe(
    query: str,
    params: tuple = (),
) -> pd.DataFrame:
    """
    Execute query and return pandas DataFrame.
    """

    conn = get_connection()

    return pd.read_sql_query(
        query,
        conn,
        params=params,
    )


# ==========================================================
# DATABASE HELPERS
# ==========================================================

def table_exists(
    table_name: str,
) -> bool:

    sql = """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    AND name=?
    """

    return fetchone(
        sql,
        (table_name,),
    ) is not None


def index_exists(
    index_name: str,
) -> bool:

    sql = """
    SELECT name
    FROM sqlite_master
    WHERE type='index'
    AND name=?
    """

    return fetchone(
        sql,
        (index_name,),
    ) is not None


def list_tables() -> list[str]:

    rows = fetchall("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
    """)

    return [r["name"] for r in rows]


def row_count(
    table_name: str,
) -> int:

    sql = f"SELECT COUNT(*) FROM {table_name}"

    value = execute_scalar(sql)

    return int(value or 0)


def database_size() -> int:
    """
    Database size in bytes.
    """

    if not DB_PATH.exists():
        return 0

    return DB_PATH.stat().st_size


# ==========================================================
# DATABASE MAINTENANCE
# ==========================================================

def database_health() -> bool:
    """
    SQLite integrity check.
    """

    try:

        result = execute_scalar(
            "PRAGMA integrity_check;"
        )

        return str(result).lower() == "ok"

    except Exception:

        logger.exception(
            "Integrity check failed."
        )

        return False


def vacuum_database() -> None:
    """
    Rebuild database.
    """

    conn = get_connection()

    conn.commit()

    _execute_with_retry(
        conn.execute,
        "VACUUM;"
    )

    logger.info(
        "VACUUM completed."
    )


def analyze_database() -> None:
    """
    Refresh SQLite statistics.
    """

    with get_db() as conn:

        _execute_with_retry(
            conn.execute,
            "ANALYZE;"
        )

    logger.info(
        "ANALYZE completed."
    )


def optimize_database() -> None:
    """
    Run SQLite optimization.
    """

    with get_db() as conn:

        _execute_with_retry(
            conn.execute,
            "PRAGMA optimize;"
        )

    logger.info(
        "Database optimized."
    )


# ==========================================================
# BACKUP
# ==========================================================

def backup_database(
    destination: str | Path,
) -> Path:
    """
    Backup current database.
    """

    destination = Path(destination)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    source = get_connection()

    backup = sqlite3.connect(
        destination,
    )

    try:

        source.backup(
            backup,
        )

        backup.commit()

    finally:

        backup.close()

    logger.info(
        "Database backup created: %s",
        destination,
    )

    return destination


# ==========================================================
# INFORMATION
# ==========================================================

def database_information() -> dict[str, Any]:

    return {

        "path": str(DB_PATH),

        "exists": DB_PATH.exists(),

        "size_bytes": database_size(),

        "healthy": database_health(),

        "tables": list_tables(),

    }


# ==========================================================
# SHUTDOWN
# ==========================================================

def shutdown() -> None:
    """
    Close current thread connection.
    """

    close_connection()

    logger.info(
        "Database connection closed."
    )


# ==========================================================
# DEBUG
# ==========================================================

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    logger.info("=" * 70)
    logger.info("GREEN BULL DATABASE")
    logger.info("=" * 70)

    print(database_information())

    print(
        "Integrity :",
        database_health(),
    )

    optimize_database()

    analyze_database()

    shutdown()

