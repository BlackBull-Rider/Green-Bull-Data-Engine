from core.db import get_connection
from indicators.calculate import add_indicators

import pandas as pd


def load_symbol(symbol):
    conn = get_connection()

    query = """
    SELECT *
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
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume"
        },
        inplace=True
    )

    df = add_indicators(df)

    cur = conn.cursor()

    for _, row in df.iterrows():

        cur.execute(
            """
            INSERT OR REPLACE INTO indicators
            (
                symbol,
                date,
                ema20,
                ema50,
                ema200,
                sma20,
                sma50,
                sma200,
                rsi,
                macd,
                macd_signal,
                macd_hist,
                bb_upper,
                bb_middle,
                bb_lower,
                stochastic_k,
                stochastic_d,
                williams_r,
                obv,
                vwap,
                volume_avg20
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                symbol,
                row["date"],
                float(row["EMA20"]) if pd.notna(row["EMA20"]) else None,
                float(row["EMA50"]) if pd.notna(row["EMA50"]) else None,
                float(row["EMA200"]) if pd.notna(row["EMA200"]) else None,
                float(row["SMA20"]) if pd.notna(row["SMA20"]) else None,
                float(row["SMA50"]) if pd.notna(row["SMA50"]) else None,
                float(row["SMA200"]) if pd.notna(row["SMA200"]) else None,
                float(row["RSI"]) if pd.notna(row["RSI"]) else None,
                float(row["MACD"]) if pd.notna(row["MACD"]) else None,
                float(row["MACD_SIGNAL"]) if pd.notna(row["MACD_SIGNAL"]) else None,
                float(row["MACD_HIST"]) if pd.notna(row["MACD_HIST"]) else None,
                float(row["BB_UPPER"]) if pd.notna(row["BB_UPPER"]) else None,
                float(row["BB_MIDDLE"]) if pd.notna(row["BB_MIDDLE"]) else None,
                float(row["BB_LOWER"]) if pd.notna(row["BB_LOWER"]) else None,
                float(row["STOCHASTIC_K"]) if pd.notna(row["STOCHASTIC_K"]) else None,
                float(row["STOCHASTIC_D"]) if pd.notna(row["STOCHASTIC_D"]) else None,
                float(row["WILLIAMS_R"]) if pd.notna(row["WILLIAMS_R"]) else None,
                float(row["OBV"]) if pd.notna(row["OBV"]) else None,
                float(row["VWAP"]) if pd.notna(row["VWAP"]) else None,
                float(row["VOLUME_AVG20"]) if pd.notna(row["VOLUME_AVG20"]) else None
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
