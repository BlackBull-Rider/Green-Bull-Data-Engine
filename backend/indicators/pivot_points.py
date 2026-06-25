import numpy as np
from typing import Dict, Any
from backend.indicators.math_utils import enforce_writeable_float_array_fast

def compile_institutional_pivots_matrix(high_v: np.ndarray, low_v: np.ndarray, close_v: np.ndarray) -> Dict[str, Any]:
    """
    [Green Bull Rider V6 - Layer 1: pivot_points]
    Computes 5 distinct institutional pivot point frameworks utilizing previous session arrays.
    Targets strictly index -1 for live core payload dispatch.
    """
    highs = enforce_writeable_float_array_fast(high_v)
    lows = enforce_writeable_float_array_fast(low_v)
    closes = enforce_writeable_float_array_fast(close_v)
    
    n = closes.shape[0]
    if n < 2:
        return {"status": "FAILED", "reason": "Insufficient elements for prior bar reference."}
        
    # Standard Floor Pivots (Referencing prior candle index -2 for latest bar execution)
    ph, pl, pc = float(highs[-2]), float(lows[-2]), float(closes[-2])
    
    # 1. Standard / Classic
    p_std = (ph + pl + pc) / 3.0
    r1_std = (2.0 * p_std) - pl
    s1_std = (2.0 * p_std) - ph
    r2_std = p_std + (ph - pl)
    s2_std = p_std - (ph - pl)
    
    # 2. CPR (Central Pivot Range)
    bc_cpr = (ph + pl) / 2.0
    tc_cpr = (2.0 * p_std) - bc_cpr
    # Ensure structural sorting for CPR bounds
    tc_final = max(tc_cpr, bc_cpr)
    bc_final = min(tc_cpr, bc_cpr)
    
    # 3. Camarilla Envelopes (High-Frequency S/R levels)
    range_width = ph - pl
    r4_cam = pc + (range_width * (1.1 / 2.0))
    r3_cam = pc + (range_width * (1.1 / 4.0))
    s3_cam = pc - (range_width * (1.1 / 4.0))
    s4_cam = pc - (range_width * (1.1 / 2.0))
    
    # 4. Woodie Pivots (Utilizes current open for calibration)
    c_open = float(highs[-1]) # Proxy to current structural anchor
    p_woodie = (ph + pl + (2.0 * pc)) / 4.0
    r1_woodie = (2.0 * p_woodie) - pl
    s1_woodie = (2.0 * p_woodie) - ph
    
    # 5. Fibonacci Retracement Levels
    r1_fib = p_std + (range_width * 0.382)
    r2_fib = p_std + (range_width * 0.618)
    s1_fib = p_std - (range_width * 0.382)
    s2_fib = p_std - (range_width * 0.618)
    
    return {
        "engine": "Institutional Pivot Point Engine v1.0_Pro",
        "standard_floor_pivots": {"R2": round(r2_std, 2), "R1": round(r1_std, 2), "PP": round(p_std, 2), "S1": round(s1_std, 2), "S2": round(s2_std, 2)},
        "central_pivot_range_cpr": {"TC": round(tc_final, 2), "Pivot": round(p_std, 2), "BC": round(bc_final, 2), "width_pct": round(((tc_final - bc_final) / p_std) * 100.0, 3)},
        "camarilla_breakout_levels": {"R4": round(r4_cam, 2), "R3": round(r3_cam, 2), "S3": round(s3_cam, 2), "S4": round(s4_cam, 2)},
        "woodie_pivots": {"R1": round(r1_woodie, 2), "PP": round(p_woodie, 2), "S1": round(s1_woodie, 2)},
        "fibonacci_pivots": {"R2": round(r2_fib, 2), "R1": round(r1_fib, 2), "S1": round(s1_fib, 2), "S2": round(s2_fib, 2)}
    }
