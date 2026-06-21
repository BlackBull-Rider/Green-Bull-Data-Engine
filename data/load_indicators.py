from core.db import get_connection
from indicators.calculate import add_indicators

import pandas as pd


def load_symbol(symbol):

    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM historical_data
        WHERE symbol=?
        ORDER BY date
        """,
        conn,
        params=(symbol,)
    )

    if df.empty:
        conn.close()
        return

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

                atr,
                adx,
                plus_di,
                minus_di,

                bb_upper,
                bb_middle,
                bb_lower,

                stochastic_k,
                stochastic_d,

                cci,
                williams_r,

                obv,
                vwap,

                volume_avg20,

                breakout_score,
                swing_score,

                supertrend,
                trend,

                pivot,
                cpr_top,
                cpr_bottom,

                r1,
                r2,
                r3,

                s1,
                s2,
                s3
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                symbol,
                row["date"],

                row.get("EMA20"),
                row.get("EMA50"),
                row.get("EMA200"),

                row.get("SMA20"),
                row.get("SMA50"),
                row.get("SMA200"),

                row.get("RSI"),

                row.get("MACD"),
                row.get("MACD_SIGNAL"),
                row.get("MACD_HIST"),

                row.get("ATR"),
                row.get("ADX"),
                row.get("PLUS_DI"),
                row.get("MINUS_DI"),

                row.get("BB_UPPER"),
                row.get("BB_MIDDLE"),
                row.get("BB_LOWER"),

                row.get("STOCHASTIC_K"),
                row.get("STOCHASTIC_D"),

                row.get("CCI"),
                row.get("WILLIAMS_R"),

                row.get("OBV"),
                row.get("VWAP"),

                row.get("VOLUME_AVG20"),

                row.get("BREAKOUT_SCORE"),
                row.get("SWING_SCORE"),

                row.get("SUPERTREND"),
                row.get("TREND"),

                row.get("PIVOT"),
                row.get("CPR_TOP"),
                row.get("CPR_BOTTOM"),

                row.get("R1"),
                row.get("R2"),
                row.get("R3"),

                row.get("S1"),
                row.get("S2"),
                row.get("S3")
            )
        )

    conn.commit()
    conn.close()

    print(symbol, "indicator saved")


def main():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT symbol
        FROM stock_master
        """
    )

    symbols = [x[0] for x in cur.fetchall()]

    conn.close()

    total = len(symbols)

    for i, symbol in enumerate(symbols, start=1):

        try:
            load_symbol(symbol)

            if i % 50 == 0:
                print(f"{i}/{total} completed")

        except Exception as e:
            print(symbol, e)


if __name__ == "__main__":
    main()
