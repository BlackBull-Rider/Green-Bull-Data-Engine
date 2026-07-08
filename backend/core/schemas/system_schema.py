"""
GREEN BULL DATA ENGINE
System Schema
"""

from __future__ import annotations

import logging
import sqlite3

logger = logging.getLogger(__name__)


def create_system_tables(conn: sqlite3.Connection) -> None:
    """
    Creates system related tables.
    Safe to run multiple times.
    """

    cursor = conn.cursor()

    # ==========================================================
    # UPDATE LOG
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS update_log (

        process_name TEXT PRIMARY KEY,

        last_run TEXT,

        status TEXT

    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_update_log_last_run
    ON update_log(last_run);
    """)

    # ==========================================================
    # PIPELINE AUDIT (Future)
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_audit (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        pipeline_name TEXT NOT NULL,

        symbol TEXT,

        stage TEXT,

        status TEXT,

        message TEXT,

        execution_time REAL,

        created_at TEXT

    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_pipeline_audit_pipeline
    ON pipeline_audit(pipeline_name);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_pipeline_audit_symbol
    ON pipeline_audit(symbol);
    """)

    # ==========================================================
    # PIPELINE STATISTICS (Future)
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pipeline_statistics (

        pipeline_name TEXT NOT NULL,

        run_date TEXT NOT NULL,

        processed_symbols INTEGER DEFAULT 0,

        failed_symbols INTEGER DEFAULT 0,

        skipped_symbols INTEGER DEFAULT 0,

        execution_time REAL,

        status TEXT,

        PRIMARY KEY (
            pipeline_name,
            run_date
        )

    );
    """)

    conn.commit()

    logger.info("System schema initialized successfully.")

