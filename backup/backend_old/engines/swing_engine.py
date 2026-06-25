import numpy as np
from typing import Dict, Any
from backend.indicators.math_utils import enforce_writeable_float_array_fast

class swing_engine:
    """
    [Green Bull Rider V6 - Engine 4: swing_engine]
    Production-Grade Structural Pivot Scanner. 100% Observation-Only.
    Detects 3-bar and 5-bar fractal swing frames and structural boundary interactions at index -1.
    """
    def __init__(self, fractal_window: int = 2) -> None:
        self.w = fractal_window # w=2 forms a 5-bar fractal block (Left 2 + Center + Right 2)

    def analyze_structural_swings(self, high_v: np.ndarray, low_v: np.ndarray, close_v: np.ndarray) -> Dict[str, Any]:
        highs = enforce_writeable_float_array_fast(high_v)
        lows = enforce_writeable_float_array_fast(low_v)
        closes = enforce_writeable_float_array_fast(close_v)
        
        n = closes.shape[0]
        min_bars = (self.w * 2) + 1
        if n < min_bars:
            return {"engine": "swing_engine", "status": "INSUFFICIENT_DATA", "raw_observations": []}
            
        observations = []
        idx = -1
        c_close = float(closes[idx])
        
        # 1. 5-Bar Fractal Swing High Detection (Target bar is index -1 - w)
        t_sh_idx = n - 1 - self.w
        is_5b_sh = True
        for i in range(1, self.w + 1):
            if highs[t_sh_idx] < highs[t_sh_idx - i] or highs[t_sh_idx] < highs[t_sh_idx + i]:
                is_5b_sh = False
                break
                
        # 2. 5-Bar Fractal Swing Low Detection
        t_sl_idx = n - 1 - self.w
        is_5b_sl = True
        for i in range(1, self.w + 1):
            if lows[t_sl_idx] > lows[t_sl_idx - i] or lows[t_sl_idx] > lows[t_sl_idx + i]:
                is_5b_sl = False
                break
                
        if is_5b_sh: observations.append(f"Validated 5-Bar Fractal Swing High Confirmed at Offset -{self.w}")
        if is_5b_sl: observations.append(f"Validated 5-Bar Fractal Swing Low Confirmed at Offset -{self.w}")
        
        # 3. 3-Bar Micro Swing Check (Target bar is index -2)
        if highs[-2] > highs[-3] and highs[-2] > highs[-1]:
            observations.append("Micro 3-Bar Swing High Formed at Offset -1")
        if lows[-2] < lows[-3] and lows[-2] < lows[-1]:
            observations.append("Micro 3-Bar Swing Low Formed at Offset -1")
            
        # 4. Immediate Structural Boundary Interaction Matrices
        recent_depth = min_bars * 3
        highest_resistance = float(np.max(highs[-recent_depth:]))
        lowest_support = float(np.max(lows[-recent_depth:])) # Reference local base floor
        
        if c_close >= highest_resistance * 0.992:
            observations.append("Price Penetrating Major Swing High Supply Barrier")
        elif c_close <= lowest_support * 1.008:
            observations.append("Price Reaching Major Swing Low Demand Barrier")
            
        return {
            "engine": "swing_engine",
            "status": "SWING_STRUCTURE_MAPPED",
            "local_extremes": {
                "rolling_peak_resistance": highest_resistance,
                "rolling_trough_support": lowest_support
            },
            "raw_observations": observations
        }
