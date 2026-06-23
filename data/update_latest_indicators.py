from core.db import get_connection


def main():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM latest_indicators
    """)

    cur.execute("""
    INSERT INTO latest_indicators
    (
        symbol,
        date,

        open,
        high,
        low,
        close,
        volume,

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

    SELECT

        i.symbol,
        i.date,

        h.open,
        h.high,
        h.low,
        h.close,
        h.volume,

        i.ema20,
        i.ema50,
        i.ema200,

        i.sma20,
        i.sma50,
        i.sma200,

        i.rsi,

        i.macd,
        i.macd_signal,
        i.macd_hist,

        i.atr,
        i.adx,
        i.plus_di,
        i.minus_di,

        i.bb_upper,
        i.bb_middle,
        i.bb_lower,

        i.stochastic_k,
        i.stochastic_d,

        i.cci,
        i.williams_r,

        i.obv,
        i.vwap,

        i.volume_avg20,

        i.breakout_score,
        i.swing_score,

        i.supertrend,
        i.trend,

        i.pivot,
        i.cpr_top,
        i.cpr_bottom,

        i.r1,
        i.r2,
        i.r3,

        i.s1,
        i.s2,
        i.s3

    FROM indicators i

    INNER JOIN
    (
        SELECT
            symbol,
            MAX(date) AS max_date
        FROM indicators
        GROUP BY symbol
    ) x
    ON i.symbol = x.symbol
    AND i.date = x.max_date

    LEFT JOIN historical_data h
    ON h.symbol = i.symbol
    AND h.date = i.date
    """)

    conn.commit()

    cur.execute("""
    SELECT COUNT(*)
    FROM latest_indicators
    """)

    total = cur.fetchone()[0]

    conn.close()

    print(
        "LATEST INDICATORS:",
        total
    )


if __name__ == "__main__":
    main()
