import numpy as np
from typing import Dict, Any
from backend.indicators.math_utils import enforce_writeable_float_array_fast

def compute_sma_native(arr: np.ndarray, period: int) -> np.ndarray:
    """Natively computes Simple Moving Average vector via rolling convolution."""
    out = np.empty_like(arr)
    out[:] = np.nan
    if arr.shape[0] < period:
        return out
    ret = np.cumsum(arr, dtype=float)
    ret[period:] = ret[period:] - ret[:-period]
    out[period - 1:] = ret[period - 1:] / period
    return out

def compute_ema_native(arr: np.ndarray, period: int) -> np.ndarray:
    """Natively computes Exponential Moving Average vector using dynamic alpha multipliers."""
    out = np.empty_like(arr)
    out[:] = np.nan
    n = arr.shape[0]
    if n < period:
        return out
    
    alpha = 2.0 / (period + 1.0)
    sma_seed = np.mean(arr[:period])
    out[period - 1] = sma_seed
    
    for i in range(period, n):
        out[i] = (arr[i] * alpha) + (out[i - 1] * (1.0 - alpha))
    return out

def compute_wma_native(arr: np.ndarray, period: int) -> np.ndarray:
    """Natively computes Weighted Moving Average vector."""
    out = np.empty_like(arr)
    out[:] = np.nan
    if arr.shape[0] < period:
        return out
    weights = np.arange(1, period + 1, dtype=float)
    weight_sum = weights.sum()
    for i in range(period - 1, arr.shape[0]):
        out[i] = np.dot(arr[i - period + 1 : i + 1], weights) / weight_sum
    return out

def compute_hma_native(arr: np.ndarray, period: int) -> np.ndarray:
    """Natively computes Hull Moving Average vector to eliminate lag efficiency."""
    n = arr.shape[0]
    out = np.empty_like(arr)
    out[:] = np.nan
    if n < period:
        return out
        
    half_p = int(period / 2)
    sqrt_p = int(np.sqrt(period))
    
    wma_half = compute_wma_native(arr, half_p)
    wma_full = compute_wma_native(arr, period)
    
    raw_diff = (2.0 * wma_half) - wma_full
    out = compute_wma_native(raw_diff, sqrt_p)
    return out

def compute_zlema_native(arr: np.ndarray, period: int) -> np.ndarray:
    """Natively computes Zero Lag Exponential Moving Average vector."""
    lag = int((period - 1) / 2)
    n = arr.shape[0]
    out = np.empty_like(arr)
    out[:] = np.nan
    if n < (period + lag):
        return out
        
    adjusted_data = arr + (arr - np.roll(arr, lag))
    adjusted_data[:lag] = arr[:lag]
    
    return compute_ema_native(adjusted_data, period)

def compute_kama_native(arr: np.ndarray, period: int = 10, fast_p: int = 2, slow_p: int = 30) -> np.ndarray:
    """Natively computes Kaufman's Adaptive Moving Average based on Efficiency Ratio."""
    n = arr.shape[0]
    out = np.empty_like(arr)
    out[:] = np.nan
    if n < period:
        return out
        
    fast_sc = 2.0 / (fast_p + 1.0)
    slow_sc = 2.0 / (slow_p + 1.0)
    
    out[period - 1] = arr[period - 1]
    
    for i in range(period, n):
        signal = abs(arr[i] - arr[i - period])
        noise = np.sum(abs(arr[i - period + 1 : i + 1] - arr[i - period : i]))
        er = signal / noise if noise != 0 else 0.0
        
        sc = (er * (fast_sc - slow_sc) + slow_sc) ** 2
        out[i] = out[i - 1] + sc * (arr[i] - out[i - 1])
    return out

def compile_moving_average_intelligence_matrix(close_array: np.ndarray) -> Dict[str, Any]:
    """Compiles native moving average baselines referencing strictly the latest date row (-1)."""
    prices = enforce_writeable_float_array_fast(close_array)
    
    if prices.shape[0] < 50:
        return {"status": "FAILED_COMPILATION", "reason": "Insufficient elements for structural baseline."}
        
    sma_20 = compute_sma_native(prices, 20)
    ema_50 = compute_ema_native(prices, 50)
    hma_20 = compute_hma_native(prices, 20)
    zlema_20 = compute_zlema_native(prices, 20)
    kama_20 = compute_kama_native(prices, 20)
    
    idx = -1
    c_close = float(prices[idx])
    
    return {
        "engine": "Moving Average Intelligence Cluster v1.0_Pro",
        "baselines": {
            "sma_20": float(round(sma_20[idx], 2)) if not np.isnan(sma_20[idx]) else None,
            "ema_50": float(round(ema_50[idx], 2)) if not np.isnan(ema_50[idx]) else None,
            "hull_ma_20": float(round(hma_20[idx], 2)) if not np.isnan(hma_20[idx]) else None,
            "zero_lag_ema_20": float(round(zlema_20[idx], 2)) if not np.isnan(zlema_20[idx]) else None,
            "kaufman_adaptive_ma_20": float(round(kama_20[idx], 2)) if not np.isnan(kama_20[idx]) else None
        },
        "structural_price_bias": "ABOVE_BASIFICATION" if c_close >= sma_20[idx] else "BELOW_BASIFICATION"
    }
