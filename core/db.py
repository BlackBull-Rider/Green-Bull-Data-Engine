import sqlite3
from pathlib import Path

DB_DIR = Path("database")
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "market.db"


def get_connection():
    return sqlite3.connect(DB_PATH)
