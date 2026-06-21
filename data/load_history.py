from providers.yahoo_provider import YahooProvider
from core.db import get_connection


def save_history(symbol, df):

    conn = get_connection()
    cur = conn.cursor()

    for date, row in df.iterrows():

        cur.execute(
            """
            INSERT OR REPLACE INTO historical_data
            (
                symbol,
                date,
                open,
                high,
                low,
                close,
                volume
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                symbol,
                str(date.date()),
                float(row["Open"]),
                float(row["High"]),
                float(row["Low"]),
                float(row["Close"]),
                float(row["Volume"])
            )
        )

    conn.commit()
    conn.close()


def load_symbol(symbol):

    provider = YahooProvider()

    df = provider.get_history(symbol)

    if df is None or len(df) == 0:
        print(f"{symbol} no data")
        return

    save_history(symbol, df)

    print(f"{symbol} saved : {len(df)} rows")


def main():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT symbol
        FROM stock_master
        ORDER BY symbol
        """
    )

    symbols = [row[0] for row in cur.fetchall()]

    conn.close()

    print(f"Found {len(symbols)} symbols")

    for i, symbol in enumerate(symbols, 1):

        try:

            load_symbol(symbol)

            if i % 50 == 0:
                print(f"{i}/{len(symbols)} completed")

        except Exception as e:

            print(symbol, e)


if __name__ == "__main__":
    main()
