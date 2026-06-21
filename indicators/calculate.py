import pandas as pd
import numpy as np


def add_indicators(df):

    df = df.copy()

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    # =====================
    # Volume Average
    # =====================
    df["VOLUME_AVG20"] = volume.rolling(20).mean()

    # =====================
    # EMA
    # =====================
    df["EMA20"] = close.ewm(span=20, adjust=False).mean()
    df["EMA50"] = close.ewm(span=50, adjust=False).mean()
    df["EMA200"] = close.ewm(span=200, adjust=False).mean()

    # =====================
    # SMA
    # =====================
    df["SMA20"] = close.rolling(20).mean()
    df["SMA50"] = close.rolling(50).mean()
    df["SMA200"] = close.rolling(200).mean()

    # =====================
    # RSI
    # =====================
    delta = close.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # =====================
    # MACD
    # =====================
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()

    df["MACD"] = ema12 - ema26
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_HIST"] = df["MACD"] - df["MACD_SIGNAL"]

    # =====================
    # Bollinger Bands
    # =====================
    bb_mid = close.rolling(20).mean()
    bb_std = close.rolling(20).std()

    df["BB_MIDDLE"] = bb_mid
    df["BB_UPPER"] = bb_mid + (2 * bb_std)
    df["BB_LOWER"] = bb_mid - (2 * bb_std)

    # =====================
    # ATR
    # =====================
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    df["ATR"] = tr.rolling(14).mean()

    # =====================
    # ADX
    # =====================
    plus_dm = high.diff()
    minus_dm = -low.diff()

    plus_dm = np.where(
        (plus_dm > minus_dm) & (plus_dm > 0),
        plus_dm,
        0
    )

    minus_dm = np.where(
        (minus_dm > plus_dm) & (minus_dm > 0),
        minus_dm,
        0
    )

    atr = df["ATR"]

    plus_di = (
        pd.Series(plus_dm).rolling(14).sum()
        / atr
    ) * 100

    minus_di = (
        pd.Series(minus_dm).rolling(14).sum()
        / atr
    ) * 100

    dx = (
        abs(plus_di - minus_di)
        / (plus_di + minus_di)
    ) * 100

    df["PLUS_DI"] = plus_di
    df["MINUS_DI"] = minus_di
    df["ADX"] = dx.rolling(14).mean()

    # =====================
    # Stochastic
    # =====================
    high14 = high.rolling(14).max()
    low14 = low.rolling(14).min()

    df["STOCHASTIC_K"] = (
        (close - low14)
        / (high14 - low14)
    ) * 100

    df["STOCHASTIC_D"] = (
        df["STOCHASTIC_K"]
        .rolling(3)
        .mean()
    )

    # =====================
    # Williams %R
    # =====================
    df["WILLIAMS_R"] = (
        (high14 - close)
        / (high14 - low14)
    ) * -100

    # =====================
    # OBV
    # =====================
    df["OBV"] = (
        np.sign(close.diff())
        .fillna(0)
        .mul(volume)
        .cumsum()
    )

    # =====================
    # VWAP
    # =====================
    df["VWAP"] = (
        (close * volume).cumsum()
        / volume.cumsum()
    )

    # =====================
    # Supertrend
    # =====================
    hl2 = (high + low) / 2

    upperband = hl2 + (3 * df["ATR"])
    lowerband = hl2 - (3 * df["ATR"])

    supertrend = []

    for i in range(len(df)):
        if i == 0:
            supertrend.append(close.iloc[i])
        else:
            if close.iloc[i] > upperband.iloc[i - 1]:
                supertrend.append(lowerband.iloc[i])
            else:
                supertrend.append(upperband.iloc[i])

    df["SUPERTREND"] = supertrend

    df["TREND"] = np.where(
        close > df["SUPERTREND"],
        "BULLISH",
        "BEARISH"
    )

    # =====================
    # Pivot
    # =====================
    pivot = (high + low + close) / 3

    bc = (high + low) / 2
    tc = (pivot - bc) + pivot

    df["PIVOT"] = pivot
    df["CPR_TOP"] = tc
    df["CPR_BOTTOM"] = bc

    # Resistance
    df["R1"] = (2 * pivot) - low
    df["R2"] = pivot + (high - low)
    df["R3"] = high + 2 * (pivot - low)

    # Support
    df["S1"] = (2 * pivot) - high
    df["S2"] = pivot - (high - low)
    df["S3"] = low - 2 * (high - pivot)

    # =====================
    # Breakout Score
    # =====================
    df["BREAKOUT_SCORE"] = np.where(
        (
            (close > df["EMA50"])
            & (df["RSI"] > 60)
            & (volume > df["VOLUME_AVG20"])
        ),
        100,
        0
    )

    # =====================
    # Swing Score
    # =====================
    df["SWING_SCORE"] = np.where(
        (
            (close > df["EMA20"])
            & (df["EMA20"] > df["EMA50"])
            & (df["RSI"] > 55)
        ),
        100,
        0
    )

    return df
