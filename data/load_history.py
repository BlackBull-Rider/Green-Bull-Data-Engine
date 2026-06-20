from providers.yahoo_provider import (
    YahooProvider
)

from core.db import get_connection


def save_history(
    symbol,
    df
):

    conn = get_connection()

    cur = conn.cursor()

    for date, row in df.iterrows():

        cur.execute(
            """
            INSERT OR REPLACE INTO
            historical_data
            (
                symbol,
                date,
                open,
                high,
                low,
                close,
                volume
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?)
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


def main():

    symbol = "RELIANCE"

    provider = YahooProvider()

    df = provider.get_history(
        symbol
    )

    save_history(
        symbol,
        df
    )

    print(
        f"{symbol} saved : {len(df)} rows"
    )


if __name__ == "__main__":
    main()
