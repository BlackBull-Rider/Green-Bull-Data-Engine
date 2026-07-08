"""
NEW AI BULL V1

Stock Master Schema Migration

Safe Migration
Python 3.13
"""

from __future__ import annotations

import logging

from backend.core.db import get_db

logger = logging.getLogger(__name__)


def column_exists(conn, table: str, column: str) -> bool:

    rows = conn.execute(
        f"PRAGMA table_info({table})"
    ).fetchall()

    return any(row["name"] == column for row in rows)


def main():

    with get_db() as conn:

        if not column_exists(
            conn,
            "stock_master",
            "status",
        ):

            conn.execute(
                """
                ALTER TABLE stock_master
                ADD COLUMN status TEXT
                DEFAULT 'ACTIVE'
                """
            )

            logger.info(
                "Added column : status"
            )

        if not column_exists(
            conn,
            "stock_master",
            "updated_at",
        ):

            conn.execute(
                """
                ALTER TABLE stock_master
                ADD COLUMN updated_at TEXT
                """
            )

            logger.info(
                "Added column : updated_at"
            )

        conn.execute(
            """
            UPDATE stock_master

            SET status='ACTIVE'

            WHERE status IS NULL
            """
        )

    print("Migration Completed.")


if __name__ == "__main__":

    main()

