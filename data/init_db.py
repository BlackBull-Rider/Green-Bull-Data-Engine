from core.db import get_connection


def create_tables():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS historical_data(

        symbol TEXT,
        date TEXT,

        open REAL,
        high REAL,
        low REAL,
        close REAL,

        volume REAL,

        PRIMARY KEY(
            symbol,
            date
        )
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_tables()

    print("Database Ready")
