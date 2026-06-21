from providers.yahoo_provider import YahooProvider
from core.db import get_connection


def save_fundamental(symbol, data):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS fundamental_data (
        symbol TEXT PRIMARY KEY,
        market_cap REAL,
        pe REAL,
        pb REAL,
        roe REAL,
        dividend_yield REAL,
        eps REAL,
        book_value REAL
    )
    """)

    cur.execute("""
    INSERT OR REPLACE INTO fundamental_data
    (
        symbol,
        market_cap,
        pe,
        pb,
        roe,
        dividend_yield,
        eps,
        book_value
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (
        symbol,
        data.get("market_cap"),
        data.get("pe"),
        data.get("pb"),
        data.get("roe"),
        data.get("dividend_yield"),
        data.get("eps"),
        data.get("book_value")
    ))

    conn.commit()
    conn.close()


def load_symbol(symbol):

    provider = YahooProvider()

    data = provider.get_fundamentals(symbol)

    save_fundamental(symbol, data)

    print(symbol, "fundamental saved")


def main():

    symbols = [
        "RELIANCE",
        "TCS",
        "INFY",
        "HDFCBANK",
        "ICICIBANK",
        "SBIN"
    ]

    for symbol in symbols:
        try:
            load_symbol(symbol)
        except Exception as e:
            print(symbol, e)


if __name__ == "__main__":
    main()
