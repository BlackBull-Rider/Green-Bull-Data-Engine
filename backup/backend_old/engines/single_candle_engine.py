import numpy as np
from typing import Dict, Any

class SingleCandleEngine:
    """
    [Green Bull Rider V6 - Layer 2: Engine 1]
    Strictly Observation-Only Framework. 100% Read-Only Architecture.
    Decodes 17 structural candle archetypes and 6 geometric matrices at index -1.
    """
    def __init__(self, atr_multiplier: float = 1.5, volume_multiplier: float = 1.5) -> None:
        self.atr_mult = atr_multiplier
        self.vol_mult = volume_multiplier

    def analyze_candle_mechanics(
        self, 
        open_v: np.ndarray, 
        high_v: np.ndarray, 
        low_v: np.ndarray, 
        close_v: np.ndarray, 
        volume_v: np.ndarray, 
        atr_v: np.ndarray
    ) -> Dict[str, Any]:
        
        n = close_v.shape[0]
        if n < 20:
            return {
                "single_candle_engine": "v1.1",
                "status": "FAILED_INSUFFICIENT_DEPTH",
                "active_candles_detected": [],
                "current_candle_metrics": {}
            }
            
        idx = -1
        o, h, l, c, v = float(open_v[idx]), float(high_v[idx]), float(low_v[idx]), float(close_v[idx]), float(volume_v[idx])
        c_atr = float(atr_v[idx]) if not np.isnan(atr_v[idx]) else (h - l if (h - l) != 0 else 1.0)
        
        spread = h - l if (h - l) != 0.0 else 1e-7
        body = abs(c - o)
        upper_wick = h - max(o, c)
        lower_wick = min(o, c) - l
        
        # 6 Core Mandated Matrix Calculations
        body_pct = (body / spread) * 100.0
        upper_wick_pct = (upper_wick / spread) * 100.0
        lower_wick_pct = (lower_wick / spread) * 100.0
        close_position = (c - l) / spread
        atr_normalized_body = body / c_atr if c_atr > 0 else 0.0
        
        v_mean_20 = float(np.mean(volume_v[-20:]))
        vol_normalized_body = body * (v / v_mean_20) if v_mean_20 > 0 else 0.0
        
        active_candles = []
        is_bull, is_bear = c > o, c < o
        
        # --- 17 UNIQUE ARCHETYPES SCANNER ---
        if body_pct <= 10.0:
            if upper_wick_pct >= 70.0: active_candles.append({"type": "Gravestone Doji", "is_mitigated": False})
            elif lower_wick_pct >= 70.0: active_candles.append({"type": "Dragonfly Doji", "is_mitigated": False})
            elif upper_wick_pct >= 40.0 and lower_wick_pct >= 40.0: active_candles.append({"type": "Long Leg Doji", "is_mitigated": False})
            else: active_candles.append({"type": "Standard Doji", "is_mitigated": False})
                
        if lower_wick >= (body * 2.0) and upper_wick_pct <= 15.0:
            active_candles.append({"type": "Hammer" if is_bull else "Hanging Man", "strength": "High"})
        if upper_wick >= (body * 2.0) and lower_wick_pct <= 15.0:
            active_candles.append({"type": "Inverted Hammer" if is_bull else "Shooting Star", "strength": "High"})
                
        if body_pct >= 90.0: 
            active_candles.append({"type": "Marubozu", "direction": "Bullish" if is_bull else "Bearish"})
        if body_pct <= 35.0 and upper_wick_pct >= 30.0 and lower_wick_pct >= 30.0: 
            active_candles.append({"type": "Spinning Top"})
            
        if spread >= (1.3 * c_atr): active_candles.append({"type": "Long Candle"})
        elif spread <= (0.6 * c_atr): active_candles.append({"type": "Short Candle"})
            
        if spread > (self.atr_mult * c_atr): active_candles.append({"type": "Wide Range Candle"})
        elif spread < (0.55 * c_atr): active_candles.append({"type": "Narrow Range Candle"})
            
        if v >= (v_mean_20 * self.vol_mult) and body_pct >= 65.0: 
            active_candles.append({"type": "Momentum Candle", "has_institutional_displacement": True})
        if v >= (v_mean_20 * 2.2) and body_pct <= 20.0:
            active_candles.append({"type": "Exhaustion Candle"})
            active_candles.append({"type": "Absorption Candle"})
            
        if (close_position > 0.85 and is_bear) or (close_position < 0.12 and is_bull): 
            active_candles.append({"type": "Trap Candle", "is_liquidity_grab": True})
            
        return {
            "single_candle_engine": "v1.1",
            "active_candles_detected": active_candles,
            "current_candle_metrics": {
                "body_to_atr_ratio": float(round(atr_normalized_body, 2)),
                "body_pct": float(round(body_pct, 2)),
                "upper_wick_pct": float(round(upper_wick_pct, 2)),
                "lower_wick_pct": float(round(lower_wick_pct, 2)),
                "close_position_idx": float(round(close_position, 2)),
                "volume_expansion_ratio": float(round(v / v_mean_20, 2)) if v_mean_20 > 0 else 1.0
            }
        }
