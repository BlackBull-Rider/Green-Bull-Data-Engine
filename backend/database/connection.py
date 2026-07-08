"""
============================================================
Green Bull Rider V6
Database Connection Manager
============================================================
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from threading import Lock
from typing import Optional


class DatabaseConnection:
    """
    Thread-safe SQLite connection manager.

    Example
    -------
    db = DatabaseConnection("database/market.db")

    with db.get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM historical_data LIMIT 5")
    """

    _lock = Lock()

    def __init__(self, database_path: str | Path):

        self.database_path = Path(database_path).expanduser().resolve()

        if not self.database_path.exists():
            raise FileNotFoundError(
                f"Database not found : {self.database_path}"
            )

        self._connection: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:

        with self._lock:

            if self._connection is None:

                self._connection = sqlite3.connect(
                    self.database_path,
                    check_same_thread=False,
                )

                self._connection.row_factory = sqlite3.Row

                self._connection.execute("PRAGMA journal_mode=WAL;")
                self._connection.execute("PRAGMA synchronous=NORMAL;")
                self._connection.execute("PRAGMA foreign_keys=ON;")
                self._connection.execute("PRAGMA temp_store=MEMORY;")
                self._connection.execute("PRAGMA cache_size=-100000;")

            return self._connection

    def get_connection(self) -> sqlite3.Connection:

        return self.connect()

    def cursor(self) -> sqlite3.Cursor:

        return self.connect().cursor()

    def commit(self) -> None:

        self.connect().commit()

    def rollback(self) -> None:

        self.connect().rollback()

    def close(self) -> None:

        with self._lock:

            if self._connection is not None:

                self._connection.close()

                self._connection = None

    def __enter__(self):

        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type:

            self.rollback()

        else:

            self.commit()

        self.close()
