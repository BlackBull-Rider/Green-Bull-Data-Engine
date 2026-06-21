from core.db import get_connection
from indicators.calculate import add_ema

import pandas as pd


def load_symbol(symbol):
    conn = get_connection()

    query = """
    SELECT date, close
    FROM historical_data
    WHERE symbol = ?
    ORDER BY date
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(symbol,)
    )

    df.rename(
        columns={
            "close": "Close"
        },
        inplace=True
    )

    df = add_ema(df)

    cur = conn.cursor()

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT OR REPLACE INTO indicators
            (
                symbol,
                date,
                ema20,
                ema50
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                symbol,
                row["date"],
                float(row["EMA20"]),
                float(row["EMA50"])
            )
        )

    conn.commit()
    conn.close()

    print(symbol, "indicator saved")

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
        load_symbol(symbol)

if __name__ == "__main__":
    main()
