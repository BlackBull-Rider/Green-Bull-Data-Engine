import numpy as np
from typing import Dict, Any
from backend.indicators.math_utils import enforce_writeable_float_array_fast

def compile_institutional_trend_pivots(high_v: np.ndarray, low_v: np.ndarray, close_v: np.ndarray) -> Dict[str, Any]:
    """
    [Green Bull Rider V6 - Layer 1: trend]
    Natively computes standard, CPR, Camarilla, Woodie, and Fibonacci pivot blocks.
    Strictly orders references targeting index -1 for dynamic matrix emission.
    """
    highs = enforce_writeable_float_array_fast(high_v)
    lows = enforce_writeable_float_array_fast(low_v)
    closes = enforce_writeable_float_array_fast(close_v)
    
    n = closes.shape[0]
    if n < 2:
        return {
            "engine": "Trend Pivot Matrix Structural Core",
            "status": "FAILED_INSUFFICIENT_DEPTH",
            "standard_floor_pivots": {},
            "central_pivot_range_cpr": {},
            "camarilla_levels": {},
            "woodie_pivots": {},
            "fibonacci_pivots": {}
        }
        
    # Standard Floor Levels referencing prior completed bar (index -2)
    ph, pl, pc = float(highs[-2]), float(lows[-2]), float(closes[-2])
    range_width = ph - pl
    
    # 1. Standard / Classic Floor
    p_std = (ph + pl + pc) / 3.0
    r1_std = (2.0 * p_std) - pl
    s1_std = (2.0 * p_std) - ph
    r2_std = p_std + range_width
    s2_std = p_std - range_width
    
    # 2. Central Pivot Range (CPR)
    bc_cpr = (ph + pl) / 2.0
    tc_cpr = (2.0 * p_std) - bc_cpr
    tc_final = max(tc_cpr, bc_cpr)
    bc_final = min(tc_cpr, bc_cpr)
    cpr_width_pct = ((tc_final - bc_final) / p_std) * 100.0 if p_std > 0 else 0.0
    
    # 3. Camarilla Overlays
    r4_cam = pc + (range_width * (1.1 / 2.0))
    r3_cam = pc + (range_width * (1.1 / 4.0))
    s3_cam = pc - (range_width * (1.1 / 4.0))
    s4_cam = pc - (range_width * (1.1 / 2.0))
    
    # 4. Woodie Grid Calibration
    p_woodie = (ph + pl + (2.0 * pc)) / 4.0
    r1_woodie = (2.0 * p_woodie) - pl
    s1_woodie = (2.0 * p_woodie) - ph
    
    # 5. Fibonacci Thresholds
    r1_fib = p_std + (range_width * 0.382)
    r2_fib = p_std + (range_width * 0.618)
    s1_fib = p_std - (range_width * 0.382)
    s2_fib = p_std - (range_width * 0.618)
    
    return {
        "engine": "Trend Pivot Matrix Structural Core",
        "status": "SUCCESS_DATA_LOCKED",
        "standard_floor_pivots": {
            "R2": float(round(r2_std, 2)),
            "R1": float(round(r1_std, 2)),
            "PP": float(round(p_std, 2)),
            "S1": float(round(s1_std, 2)),
            "S2": float(round(s2_std, 2))
        },
        "central_pivot_range_cpr": {
            "TC": float(round(tc_final, 2)),
            "Pivot": float(round(p_std, 2)),
            "BC": float(round(bc_final, 2)),
            "width_percentage": float(round(cpr_width_pct, 3))
        },
        "camarilla_levels": {
            "R4": float(round(r4_cam, 2)),
            "R3": float(round(r3_cam, 2)),
            "S3": float(round(s3_cam, 2)),
            "S4": float(round(s4_cam, 2))
        },
        "woodie_pivots": {
            "R1": float(round(r1_woodie, 2)),
            "PP": float(round(p_woodie, 2)),
            "S1": float(round(s1_woodie, 2))
        },
        "fibonacci_pivots": {
            "R2": float(round(r2_fib, 2)),
            "R1": float(round(r1_fib, 2)),
            "S1": float(round(s1_fib, 2)),
            "S2": float(round(s2_fib, 2))
        }
    }
