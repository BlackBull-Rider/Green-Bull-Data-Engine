# init_db.py

from core.db import get_connection


def create_tables():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS historical_data(

        symbol TEXT NOT NULL,

        date TEXT NOT NULL,

        open REAL,
        high REAL,
        low REAL,
        close REAL,

        volume REAL,

        PRIMARY KEY(symbol,date)

    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS update_log(

        symbol TEXT PRIMARY KEY,

        last_update TEXT

    )
    """)

    conn.commit()
    conn.close()

    print("Database Ready")


if __name__ == "__main__":
    create_tables()
