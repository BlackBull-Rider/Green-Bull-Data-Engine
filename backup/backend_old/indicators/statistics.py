import numpy as np
from typing import Dict, Any
from backend.indicators.math_utils import enforce_writeable_float_array_fast

def compute_rolling_std_native(arr: np.ndarray, period: int) -> np.ndarray:
    out = np.empty_like(arr)
    out[:] = np.nan
    n = arr.shape[0]
    if n < period: return out
    for i in range(period - 1, n):
        out[i] = np.std(arr[i - period + 1 : i + 1])
    return out

def compute_linear_regression_slope_vector(arr: np.ndarray, period: int) -> np.ndarray:
    out = np.empty_like(arr)
    out[:] = np.nan
    n = arr.shape[0]
    if n < period: return out
        
    x = np.arange(period, dtype=float)
    x_mean = np.mean(x)
    x_deviations = x - x_mean
    denom = np.sum(x_deviations ** 2)
    if denom == 0: denom = 1e-7
        
    for i in range(period - 1, n):
        y = arr[i - period + 1 : i + 1]
        y_mean = np.mean(y)
        out[i] = np.sum(x_deviations * (y - y_mean)) / denom
    return out

def compute_adx_wilder_native(high_v: np.ndarray, low_v: np.ndarray, atr_v: np.ndarray, period: int = 14) -> tuple:
    """Natively computes PLUS_DI, MINUS_DI, and ADX using directional movement metrics."""
    h = enforce_writeable_float_array_fast(high_v)
    l = enforce_writeable_float_array_fast(low_v)
    atr = enforce_writeable_float_array_fast(atr_v)
    n = h.shape[0]
    
    plus_di = np.empty(n)
    minus_di = np.empty(n)
    adx = np.empty(n)
    plus_di[:] = np.nan
    minus_di[:] = np.nan
    adx[:] = np.nan
    
    if n <= period: return plus_di, minus_di, adx
    
    up_move = np.zeros(n)
    down_move = np.zeros(n)
    up_move[1:] = h[1:] - h[:-1]
    down_move[1:] = l[:-1] - l[1:]
    
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    
    alpha = 1.0 / period
    smooth_plus_dm = np.zeros(n)
    smooth_minus_dm = np.zeros(n)
    
    smooth_plus_dm[period] = np.mean(plus_dm[:period])
    smooth_minus_dm[period] = np.mean(minus_dm[:period])
    
    for i in range(period + 1, n):
        smooth_plus_dm[i] = (plus_dm[i] * alpha) + (smooth_plus_dm[i - 1] * (1.0 - alpha))
        smooth_minus_dm[i] = (minus_dm[i] * alpha) + (smooth_minus_dm[i - 1] * (1.0 - alpha))
        
    safe_atr = np.where(atr == 0, 1e-7, atr)
    plus_di = (smooth_plus_dm / safe_atr) * 100.0
    minus_di = (smooth_minus_dm / safe_atr) * 100.0
    
    denom = plus_di + minus_di
    safe_denom = np.where(denom == 0, 1e-7, denom)
    dx = (abs(plus_di - minus_di) / safe_denom) * 100.0
    
    # ADX requires double smoothing window depth
    if n > period * 2:
        adx[period * 2 - 1] = np.mean(dx[period : period * 2])
        for i in range(period * 2, n):
            adx[i] = (dx[i] * alpha) + (adx[i - 1] * (1.0 - alpha))
            
    return plus_di, minus_di, adx

def compile_statistics_intelligence_matrix(high_array: np.ndarray, low_array: np.ndarray, close_array: np.ndarray, atr_array: np.ndarray) -> Dict[str, Any]:
    closes = enforce_writeable_float_array_fast(close_array)
    std_20 = compute_rolling_std_native(closes, 20)
    slope_20 = compute_linear_regression_slope_vector(closes, 20)
    angle_20 = np.arctan(slope_20) * (180.0 / np.pi)
    
    # Calculate directional movement metrics
    plus_di, minus_di, adx = compute_adx_wilder_native(high_array, low_array, atr_array, 14)
    
    idx = -1
    return {
        "engine": "Statistical Intelligence Cluster v1.0_Pro",
        "rolling_standard_deviation_20": float(round(std_20[idx], 2)) if not np.isnan(std_20[idx]) else 0.0,
        "linear_regression_slope_20": float(round(slope_20[idx], 4)) if not np.isnan(slope_20[idx]) else 0.0,
        "mathematical_trend_angle_degrees": float(round(angle_20[idx], 2)) if not np.isnan(angle_20[idx]) else 0.0,
        "directional_movement_index": {
            "PLUS_DI": float(round(plus_di[idx], 2)) if not np.isnan(plus_di[idx]) else None,
            "MINUS_DI": float(round(minus_di[idx], 2)) if not np.isnan(minus_di[idx]) else None,
            "ADX_Trend_Strength": float(round(adx[idx], 2)) if not np.isnan(adx[idx]) else None
        },
        "statistical_bias": "BULLISH_EXPANSION" if slope_20[idx] > 0 else "BEARISH_CONTRACTION"
    }

