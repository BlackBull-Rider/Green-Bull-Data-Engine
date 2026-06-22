from providers.yahoo_provider import YahooProvider
from core.db import get_connection


provider = YahooProvider()


def get_last_date(symbol):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT MAX(date)
        FROM historical_data
        WHERE symbol=?
        """,
        (symbol,)
    )

    row = cur.fetchone()

    conn.close()

    return row[0]


def save_rows(symbol, df):

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


def sync_symbol(symbol):

    last_date = get_last_date(symbol)

    df = provider.get_history(
        symbol,
        period="10d"
    )

    if df is None or len(df) == 0:
        return

    if last_date:

        df = df[
            df.index.strftime("%Y-%m-%d")
            > last_date
        ]

    if len(df):

        save_rows(symbol, df)

        print(
            symbol,
            "added",
            len(df),
            "candles"
        )


def main():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT symbol
        FROM stock_master
        """
    )

    symbols = [
        x[0]
        for x in cur.fetchall()
    ]

    conn.close()

    for i, symbol in enumerate(symbols, 1):

        try:

            sync_symbol(symbol)

            if i % 100 == 0:

                print(
                    f"{i}/{len(symbols)}"
                )

        except Exception as e:

            print(symbol, e)


if __name__ == "__main__":
    main()
