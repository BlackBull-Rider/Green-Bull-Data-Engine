import pandas as pd
import numpy as np


def add_indicators(df):

    df = df.copy()

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    volume = df["Volume"]

    # =====================
    # Volume
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
    # RSI (Wilder)
    # =====================

    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/14, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

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
    # Bollinger
    # =====================

    bb_mid = close.rolling(20).mean()
    bb_std = close.rolling(20).std()

    df["BB_MIDDLE"] = bb_mid
    df["BB_UPPER"] = bb_mid + (2 * bb_std)
    df["BB_LOWER"] = bb_mid - (2 * bb_std)

    # =====================
    # ATR (Wilder)
    # =====================

    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    df["ATR"] = tr.ewm(alpha=1/14, adjust=False).mean()

    # =====================
    # ADX (Wilder)
    # =====================

    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = np.where(
        (up_move > down_move) & (up_move > 0),
        up_move,
        0.0
    )

    minus_dm = np.where(
        (down_move > up_move) & (down_move > 0),
        down_move,
        0.0
    )

    plus_dm = pd.Series(plus_dm, index=df.index)
    minus_dm = pd.Series(minus_dm, index=df.index)

    atr = df["ATR"]

    plus_di = (
        plus_dm.ewm(alpha=1/14, adjust=False).mean()
        / atr
    ) * 100

    minus_di = (
        minus_dm.ewm(alpha=1/14, adjust=False).mean()
        / atr
    ) * 100

    dx = (
        (plus_di - minus_di).abs()
        / (plus_di + minus_di)
    ) * 100

    adx = dx.ewm(alpha=1/14, adjust=False).mean()

    df["PLUS_DI"] = plus_di
    df["MINUS_DI"] = minus_di
    df["ADX"] = adx

    # =====================
    # STOCHASTIC
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
    # WILLIAMS %R
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
    # SUPERTREND
    # =====================

    multiplier = 3.0

    hl2 = (high + low) / 2

    basic_upper = hl2 + (multiplier * df["ATR"])
    basic_lower = hl2 - (multiplier * df["ATR"])

    final_upper = basic_upper.copy()
    final_lower = basic_lower.copy()

    for i in range(1, len(df)):

        if (
            basic_upper.iloc[i] < final_upper.iloc[i - 1]
            or close.iloc[i - 1] > final_upper.iloc[i - 1]
        ):
            final_upper.iloc[i] = basic_upper.iloc[i]
        else:
            final_upper.iloc[i] = final_upper.iloc[i - 1]

        if (
            basic_lower.iloc[i] > final_lower.iloc[i - 1]
            or close.iloc[i - 1] < final_lower.iloc[i - 1]
        ):
            final_lower.iloc[i] = basic_lower.iloc[i]
        else:
            final_lower.iloc[i] = final_lower.iloc[i - 1]

    supertrend = pd.Series(index=df.index, dtype=float)
    trend = []

    for i in range(len(df)):

        if i == 0:
            supertrend.iloc[i] = final_lower.iloc[i]
            trend.append("BULLISH")
            continue

        prev_st = supertrend.iloc[i - 1]

        if prev_st == final_upper.iloc[i - 1]:

            if close.iloc[i] <= final_upper.iloc[i]:
                supertrend.iloc[i] = final_upper.iloc[i]
                trend.append("BEARISH")
            else:
                supertrend.iloc[i] = final_lower.iloc[i]
                trend.append("BULLISH")

        else:

            if close.iloc[i] >= final_lower.iloc[i]:
                supertrend.iloc[i] = final_lower.iloc[i]
                trend.append("BULLISH")
            else:
                supertrend.iloc[i] = final_upper.iloc[i]
                trend.append("BEARISH")

    df["SUPERTREND"] = supertrend
    df["TREND"] = trend

    return df
