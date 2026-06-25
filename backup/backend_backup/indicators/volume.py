import numpy as np
from typing import Dict, Any
from backend.indicators.math_utils import enforce_writeable_float_array_fast
from backend.indicators.moving_average import compute_sma_native

def compile_volume_intelligence_matrix(open_array: np.ndarray, high_array: np.ndarray, low_array: np.ndarray, close_array: np.ndarray, volume_array: np.ndarray) -> Dict[str, Any]:
    """Compiles advanced volume profile distribution vectors targeting strictly index -1."""
    opens = enforce_writeable_float_array_fast(open_array)
    highs = enforce_writeable_float_array_fast(high_array)
    lows = enforce_writeable_float_array_fast(low_array)
    closes = enforce_writeable_float_array_fast(close_array)
    volumes = enforce_writeable_float_array_fast(volume_array)
    
    n = closes.shape[0]
    if n < 20:
        return {"status": "FAILED_COMPILATION", "reason": "Insufficient elements for volume vectoring."}
        
    # 1. Volume Moving Average (20 Period)
    v_ma20 = compute_sma_native(volumes, 20)
    
    # 2. On-Balance Volume (OBV) Vector Calculation
    obv = np.zeros_like(closes)
    obv[0] = volumes[0]
    for i in range(1, n):
        if closes[i] > closes[i - 1]:
            obv[i] = obv[i - 1] + volumes[i]
        elif closes[i] < closes[i - 1]:
            obv[i] = obv[i - 1] - volumes[i]
        else:
            obv[i] = obv[i - 1]
            
    # 3. Chaikin Money Flow (CMF - 20 Period)
    cmf = np.empty_like(closes)
    cmf[:] = np.nan
    
    # Money Flow Multiplier & Volume Vectorization
    denom = highs - lows
    safe_denom = np.where(denom == 0, 1e-7, denom)
    mf_multiplier = ((closes - lows) - (highs - closes)) / safe_denom
    mf_volume = mf_multiplier * volumes
    
    for i in range(19, n):
        sum_mf_volume = np.sum(mf_volume[i - 19 : i + 1])
        sum_volume = np.sum(volumes[i - 19 : i + 1])
        cmf[i] = sum_mf_volume / sum_volume if sum_volume != 0 else 0.0
        
    idx = -1
    c_vol = float(volumes[idx])
    c_v_ma = float(v_ma20[idx]) if not np.isnan(v_ma20[idx]) else 1.0
    
    # RVOL & Institutional Spike Logic
    rvol = c_vol / c_v_ma if c_v_ma > 0 else 0.0
    volume_spike = "INSTITUTIONAL_SPIKE" if rvol >= 2.0 else ("ABOVE_AVERAGE" if rvol >= 1.3 else "NORMAL_VOLUME")
    
    return {
        "engine": "Volume Intelligence Cluster v1.0_Pro",
        "relative_volume_rvol": float(round(rvol, 2)),
        "volume_spike_state": volume_spike,
        "on_balance_volume": float(obv[idx]),
        "chaikin_money_flow_20": float(round(cmf[idx], 3)) if not np.isnan(cmf[idx]) else 0.0,
        "raw_metrics": {
            "current_volume": float(c_vol),
            "average_volume_20": float(round(c_v_ma, 2))
        }
    }
