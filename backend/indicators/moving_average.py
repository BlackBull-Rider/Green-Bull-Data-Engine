"""
=========================================================
Green Bull Rider V6
Moving Average Indicator Library
=========================================================
Author  : Green Bull Rider
Version : 1.0
=========================================================
"""

from __future__ import annotations

from typing import Final

import numpy as np

__all__: Final = [

    "sma",
    "ema",
    "wma",
    "vwma",
    "dema",
    "tema",
    "hma",
    "zlema",
    "kama",
    "alma",
    "t3",

]


# ==========================================================
# Internal Helpers
# ==========================================================

def _as_float64(data) -> np.ndarray:
    """
    Convert input to contiguous float64 NumPy array.
    """

    arr = np.asarray(data, dtype=np.float64)

    if arr.ndim != 1:
        raise ValueError("Input must be one-dimensional.")

    return np.ascontiguousarray(arr)


def _validate_period(period: int):

    if not isinstance(period, int):
        raise TypeError("period must be int")

    if period < 1:
        raise ValueError("period must be greater than zero")


# ==========================================================
# SMA
# ==========================================================

def sma(
    close,
    period: int
) -> np.ndarray:

    _validate_period(period)

    close = _as_float64(close)

    n = close.size

    out = np.full(n, np.nan)

    if n < period:
        return out

    cumsum = np.cumsum(close)

    out[period - 1] = cumsum[
        period - 1
    ] / period

    for i in range(period, n):

        out[i] = (
            cumsum[i]
            -
            cumsum[i - period]
        ) / period

    return out


# ==========================================================
# EMA
# ==========================================================

def ema(
    close,
    period: int
) -> np.ndarray:

    _validate_period(period)

    close = _as_float64(close)

    n = close.size

    out = np.full(n, np.nan)

    if n < period:
        return out

    alpha = 2.0 / (period + 1.0)

    out[period - 1] = np.mean(
        close[:period]
    )

    for i in range(period, n):

        out[i] = (
            alpha * close[i]
            +
            (1.0 - alpha)
            * out[i - 1]
        )

    return out


# ==========================================================
# WMA
# ==========================================================

def wma(
    close,
    period: int
) -> np.ndarray:

    _validate_period(period)

    close = _as_float64(close)

    n = close.size

    out = np.full(n, np.nan)

    if n < period:
        return out

    weights = np.arange(
        1,
        period + 1,
        dtype=np.float64
    )

    denominator = weights.sum()

    for i in range(
        period - 1,
        n
    ):

        window = close[
            i - period + 1:
            i + 1
        ]

        out[i] = (
            np.dot(
                window,
                weights
            )
            /
            denominator
        )

    return out

# ==========================================================
# VWMA
# ==========================================================

def vwma(
    close,
    volume,
    period: int
) -> np.ndarray:

    _validate_period(period)

    close = _as_float64(close)
    volume = _as_float64(volume)

    if close.size != volume.size:
        raise ValueError(
            "close and volume length mismatch."
        )

    n = close.size

    out = np.full(n, np.nan)

    if n < period:
        return out

    for i in range(period - 1, n):

        c = close[
            i - period + 1:i + 1
        ]

        v = volume[
            i - period + 1:i + 1
        ]

        total_volume = np.sum(v)

        if total_volume == 0:
            continue

        out[i] = np.dot(c, v) / total_volume

    return out


# ==========================================================
# DEMA
# ==========================================================

def dema(
    close,
    period: int
) -> np.ndarray:

    ema1 = ema(close, period)
    ema2 = ema(ema1, period)

    out = (2.0 * ema1) - ema2

    out[: period * 2 - 2] = np.nan

    return out


# ==========================================================
# TEMA
# ==========================================================

def tema(
    close,
    period: int
) -> np.ndarray:

    ema1 = ema(close, period)
    ema2 = ema(ema1, period)
    ema3 = ema(ema2, period)

    out = (
        3.0 * ema1
        - 3.0 * ema2
        + ema3
    )

    out[: period * 3 - 3] = np.nan

    return out


# ==========================================================
# HMA
# ==========================================================

def hma(
    close,
    period: int
) -> np.ndarray:

    _validate_period(period)

    close = _as_float64(close)

    half = max(1, period // 2)

    sqrt_period = max(
        1,
        int(np.sqrt(period))
    )

    wma_half = wma(close, half)

    wma_full = wma(close, period)

    raw = (2.0 * wma_half) - wma_full

    return wma(raw, sqrt_period)


# ==========================================================
# ZLEMA
# ==========================================================

def zlema(
    close,
    period: int
) -> np.ndarray:

    _validate_period(period)

    close = _as_float64(close)

    n = close.size

    out = np.full(n, np.nan)

    if n < period:
        return out

    lag = (period - 1) // 2

    adjusted = close.copy()

    if lag > 0:
        adjusted[lag:] = (
            close[lag:]
            +
            (
                close[lag:]
                -
                close[:-lag]
            )
        )

    return ema(adjusted, period)


# ==========================================================
# KAMA
# ==========================================================

def kama(
    close,
    period: int = 10,
    fast: int = 2,
    slow: int = 30,
) -> np.ndarray:

    _validate_period(period)

    close = _as_float64(close)

    n = close.size

    out = np.full(n, np.nan)

    if n <= period:
        return out

    fast_sc = 2.0 / (fast + 1.0)
    slow_sc = 2.0 / (slow + 1.0)

    out[period - 1] = close[period - 1]

    for i in range(period, n):

        direction = abs(
            close[i]
            -
            close[i - period]
        )

        volatility = np.sum(
            np.abs(
                np.diff(
                    close[
                        i-period:i+1
                    ]
                )
            )
        )

        er = (
            direction / volatility
            if volatility > 0
            else 0.0
        )

        sc = (
            er
            *
            (
                fast_sc
                -
                slow_sc
            )
            +
            slow_sc
        ) ** 2

        out[i] = (
            out[i - 1]
            +
            sc
            *
            (
                close[i]
                -
                out[i - 1]
            )
        )

    return out


# ==========================================================
# ALMA
# ==========================================================

def alma(
    close,
    period: int = 9,
    sigma: float = 6.0,
    offset: float = 0.85,
) -> np.ndarray:

    _validate_period(period)

    close = _as_float64(close)

    n = close.size

    out = np.full(n, np.nan)

    if n < period:
        return out

    m = offset * (period - 1)

    s = period / sigma

    weights = np.exp(
        -(
            (
                np.arange(period)
                -
                m
            ) ** 2
        )
        /
        (2.0 * s * s)
    )

    weights /= weights.sum()

    for i in range(period - 1, n):

        out[i] = np.dot(
            close[
                i-period+1:i+1
            ],
            weights
        )

    return out


# ==========================================================
# Tillson T3
# ==========================================================

def t3(
    close,
    period: int = 10,
    volume_factor: float = 0.7,
) -> np.ndarray:

    e1 = ema(close, period)
    e2 = ema(e1, period)
    e3 = ema(e2, period)
    e4 = ema(e3, period)
    e5 = ema(e4, period)
    e6 = ema(e5, period)

    v = volume_factor

    c1 = -(v ** 3)
    c2 = 3 * v * v + 3 * v ** 3
    c3 = -6 * v * v - 3 * v - 3 * v ** 3
    c4 = 1 + 3 * v + 3 * v * v + v ** 3

    out = (
        c1 * e6
        +
        c2 * e5
        +
        c3 * e4
        +
        c4 * e3
    )

    out[: period * 6] = np.nan

    return out


