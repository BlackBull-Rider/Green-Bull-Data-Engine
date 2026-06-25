import numpy as np
from typing import Dict, Any
from backend.indicators.math_utils import enforce_writeable_float_array_fast
from backend.indicators.moving_average import compute_sma_native

def compute_atr_wilder_native(high_v: np.ndarray, low_v: np.ndarray, close_v: np.ndarray, period: int = 14) -> np.ndarray:
    """Natively computes True Range & Wilder's Average True Range vector without pandas lag."""
    h = enforce_writeable_float_array_fast(high_v)
    l = enforce_writeable_float_array_fast(low_v)
    c = enforce_writeable_float_array_fast(close_v)
    n = c.shape[0]
    
    out = np.empty_like(c)
    out[:] = np.nan
    if n <= period: 
        return out
    
    tr = np.zeros(n)
    tr[0] = h[0] - l[0]
    for i in range(1, n):
        tr1 = h[i] - l[i]
        tr2 = abs(h[i] - c[i - 1])
        tr3 = abs(l[i] - c[i - 1])
        tr[i] = max(tr1, tr2, tr3)
        
    alpha = 1.0 / period
    out[period] = np.mean(tr[:period])
    for i in range(period + 1, n):
        out[i] = (tr[i] * alpha) + (out[i - 1] * (1.0 - alpha))
    return out

def compile_volatility_intelligence_matrix(high_array: np.ndarray, low_array: np.ndarray, close_array: np.ndarray) -> Dict[str, Any]:
    """Compiles complete structural volatility envelopes and compression ratios."""
    highs = enforce_writeable_float_array_fast(high_array)
    lows = enforce_writeable_float_array_fast(low_array)
    closes = enforce_writeable_float_array_fast(close_array)
    
    n = closes.shape[0]
    if n < 20:
        return {"status": "FAILED_COMPILATION", "reason": "Insufficient elements for volatility mapping."}
        
    # 1. Wilder ATR Calculation
    atr = compute_atr_wilder_native(highs, lows, closes, 14)
    
    # 2. Bollinger Bands (20 SMA, 2 Standard Deviations)
    bb_mid = compute_sma_native(closes, 20)
    bb_std = np.empty_like(closes)
    bb_std[:] = np.nan
    for i in range(19, n):
        bb_std[i] = np.std(closes[i - 19 : i + 1])
        
    bb_upper = bb_mid + (2.0 * bb_std)
    bb_lower = bb_mid - (2.0 * bb_std)
    
    # 3. Bollinger Bandwidth % Vector
    safe_mid = np.where(bb_mid == 0, 1e-7, bb_mid)
    bb_bandwidth = ((bb_upper - bb_lower) / safe_mid) * 100.0
    
    # Historical Volatility (Rolling 20-period log returns standard dev)
    hv = np.empty_like(closes)
    hv[:] = np.nan
    if n > 21:
        log_returns = np.diff(np.log(np.where(closes == 0, 1e-7, closes)))
        for i in range(19, n - 1):
            hv[i + 1] = np.std(log_returns[i - 19 : i + 1]) * np.sqrt(252) * 100.0
            
    idx = -1
    c_bandwidth = bb_bandwidth[idx]
    
    # Volatility Regime Classifier (Squeeze vs Expansion)
    if not np.isnan(c_bandwidth):
        v_mean_bandwidth = np.mean(bb_bandwidth[-100:]) if n >= 100 else np.mean(bb_bandwidth[-20:])
        regime = "COMPRESSION_SQUEEZE" if c_bandwidth < v_mean_bandwidth * 0.85 else (
            "EXPANSION_EXPLOSION" if c_bandwidth > v_mean_bandwidth * 1.20 else "NORMAL_REGIME"
        )
    else:
        regime = "UNKNOWN"
        
    return {
        "engine": "Volatility Intelligence Cluster v1.0_Pro",
        "atr_14": float(round(atr[idx], 2)) if not np.isnan(atr[idx]) else None,
        "bollinger_envelopes": {
            "upper_band": float(round(bb_upper[idx], 2)) if not np.isnan(bb_upper[idx]) else None,
            "middle_band": float(round(bb_mid[idx], 2)) if not np.isnan(bb_mid[idx]) else None,
            "lower_band": float(round(bb_lower[idx], 2)) if not np.isnan(bb_lower[idx]) else None,
            "bandwidth_pct": float(round(c_bandwidth, 2)) if not np.isnan(c_bandwidth) else None
        },
        "historical_volatility_annualized": float(round(hv[idx], 2)) if not np.isnan(hv[idx]) else None,
        "volatility_regime": regime
    }
