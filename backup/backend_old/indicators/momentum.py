import numpy as np
from typing import Dict, Any
from backend.indicators.math_utils import enforce_writeable_float_array_fast
from backend.indicators.moving_average import compute_ema_native

def compute_rsi_wilder(arr: np.ndarray, period: int = 14) -> np.ndarray:
    out = np.empty_like(arr)
    out[:] = np.nan
    n = arr.shape[0]
    if n <= period: return out
        
    delta = np.diff(arr)
    gains = np.where(delta > 0, delta, 0.0)
    losses = np.where(delta < 0, -delta, 0.0)
    
    alpha = 1.0 / period
    avg_gain = np.empty(n)
    avg_loss = np.empty(n)
    avg_gain[:] = np.nan
    avg_loss[:] = np.nan
    
    avg_gain[period] = np.mean(gains[:period])
    avg_loss[period] = np.mean(losses[:period])
    
    for i in range(period + 1, n):
        avg_gain[i] = (gains[i - 1] * alpha) + (avg_gain[i - 1] * (1.0 - alpha))
        avg_loss[i] = (losses[i - 1] * alpha) + (avg_loss[i - 1] * (1.0 - alpha))
        
    rs = avg_gain / np.where(avg_loss == 0, 1e-7, avg_loss)
    out[period:] = 100.0 - (100.0 / (1.0 + rs[period:]))
    return out

def compute_macd_safe(macd_line: np.ndarray, period: int = 9) -> np.ndarray:
    """Computes a NaN-safe Signal Line for the MACD vector."""
    out = np.empty_like(macd_line)
    out[:] = np.nan
    n = macd_line.shape[0]
    
    # Find first non-NaN index
    valid_idx = np.where(~np.isnan(macd_line))[0]
    if len(valid_idx) < period: return out
    
    start_pos = valid_idx[0] + period - 1
    if start_pos >= n: return out
    
    alpha = 2.0 / (period + 1.0)
    out[start_pos] = np.mean(macd_line[valid_idx[0]:valid_idx[0] + period])
    
    for i in range(start_pos + 1, n):
        out[i] = (macd_line[i] * alpha) + (out[i - 1] * (1.0 - alpha))
    return out

def compile_momentum_intelligence_matrix(high_array: np.ndarray, low_array: np.ndarray, close_array: np.ndarray) -> Dict[str, Any]:
    highs = enforce_writeable_float_array_fast(high_array)
    lows = enforce_writeable_float_array_fast(low_array)
    closes = enforce_writeable_float_array_fast(close_array)
    
    n = closes.shape[0]
    if n < 35:
        return {"status": "FAILED_COMPILATION", "reason": "Insufficient elements."}
        
    rsi = compute_rsi_wilder(closes, 14)
    rsi_slope = np.zeros_like(rsi)
    rsi_slope[1:] = np.diff(rsi)
    
    ema12 = compute_ema_native(closes, 12)
    ema26 = compute_ema_native(closes, 26)
    macd_line = ema12 - ema26
    
    # Run the NaN-safe MACD processing engine
    macd_signal = compute_macd_safe(macd_line, 9)
    macd_hist = macd_line - macd_signal
    
    stoch_k = np.empty(n)
    stoch_k[:] = np.nan
    williams_r = np.empty(n)
    williams_r[:] = np.nan
    
    for i in range(13, n):
        h14 = np.max(highs[i - 13 : i + 1])
        l14 = np.min(lows[i - 13 : i + 1])
        denom = h14 - l14 if (h14 - l14) != 0 else 1e-7
        stoch_k[i] = ((closes[i] - l14) / denom) * 100.0
        williams_r[i] = ((h14 - closes[i]) / denom) * -100.0
        
    stoch_d = np.empty(n)
    stoch_d[:] = np.nan
    for i in range(15, n):
        stoch_d[i] = np.mean(stoch_k[i - 2 : i + 1])
        
    idx = -1
    return {
        "engine": "Momentum Intelligence Cluster v1.0_Pro",
        "rsi_14": float(round(rsi[idx], 2)) if not np.isnan(rsi[idx]) else None,
        "rsi_slope": float(round(rsi_slope[idx], 2)) if not np.isnan(rsi_slope[idx]) else None,
        "macd_metrics": {
            "macd_line": float(round(macd_line[idx], 2)) if not np.isnan(macd_line[idx]) else None,
            "signal_line": float(round(macd_signal[idx], 2)) if not np.isnan(macd_signal[idx]) else None,
            "histogram": float(round(macd_hist[idx], 2)) if not np.isnan(macd_hist[idx]) else None
        },
        "stochastic_oscillators": {
            "stoch_k": float(round(stoch_k[idx], 2)) if not np.isnan(stoch_k[idx]) else None,
            "stoch_d": float(round(stoch_d[idx], 2)) if not np.isnan(stoch_d[idx]) else None
        },
        "williams_r_14": float(round(williams_r[idx], 2)) if not np.isnan(williams_r[idx]) else None
    }
