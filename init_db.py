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
    CREATE TABLE IF NOT EXISTS fundamental_data(

        symbol TEXT PRIMARY KEY,

        market_cap REAL,

        pe REAL,
        pb REAL,

        roe REAL,
        roce REAL,

        debt_equity REAL,

        sales_growth REAL,
        profit_growth REAL,

        promoter_holding REAL,

        institutional_holding REAL,

        fii_holding REAL,
        dii_holding REAL,

        updated_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS update_log(

        symbol TEXT PRIMARY KEY,

        last_history_update TEXT,

        last_fundamental_update TEXT

    )
    """)

    conn.commit()
    conn.close()

    print("Database Ready")


if __name__ == "__main__":
    create_tables()
