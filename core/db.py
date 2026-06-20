# core/db.py

import sqlite3
from pathlib import Path

Path("database").mkdir(exist_ok=True)

DB_PATH = "database/market.db"


def get_connection():
    return sqlite3.connect(DB_PATH)
