import numpy as np
from typing import Dict, Any
from backend.indicators.math_utils import enforce_writeable_float_array_fast

class candle_psychology_engine:
    """
    [Green Bull Rider V6 - Engine 3: candle_psychology_engine]
    Production-Grade Deep Behavioral Core. 100% Observation-Only.
    Decodes order-flow sentiment maps, traps, and retail panic liquidations at index -1.
    """
    def __init__(self, volume_threshold_multiplier: float = 1.4) -> None:
        self.vol_mult = volume_threshold_multiplier

    def decode_market_psychology(
        self, open_v: np.ndarray, high_v: np.ndarray, low_v: np.ndarray, close_v: np.ndarray, volume_v: np.ndarray,
        body_pct_v: np.ndarray, upper_wick_pct_v: np.ndarray, lower_wick_pct_v: np.ndarray
    ) -> Dict[str, Any]:
        opens = enforce_writeable_float_array_fast(open_v)
        highs = enforce_writeable_float_array_fast(high_v)
        lows = enforce_writeable_float_array_fast(low_v)
        closes = enforce_writeable_float_array_fast(close_v)
        volumes = enforce_writeable_float_array_fast(volume_v)
        body_p = enforce_writeable_float_array_fast(body_pct_v)
        u_wick_p = enforce_writeable_float_array_fast(upper_wick_pct_v)
        l_wick_p = enforce_writeable_float_array_fast(lower_wick_pct_v)
        
        if closes.shape[0] < 5:
            return {"engine": "candle_psychology_engine", "status": "INSUFFICIENT_DATA", "raw_observations": []}
            
        o0, h0, l0, c0, v0 = float(opens[-1]), float(highs[-1]), float(lows[-1]), float(closes[-1]), float(volumes[-1])
        h1, l1, c1 = float(highs[-2]), float(lows[-2]), float(closes[-2])
        
        bp0, uw0, lw0 = float(body_p[-1]), float(u_wick_p[-1]), float(l_wick_p[-1])
        v_mean = float(np.mean(volumes[-20:]))
        
        observations = []
        is_bull = c0 > o0
        spread0 = h0 - l0 if (h0 - l0) != 0 else 1e-7
        
        # 1-2. Institutional Drive/Panic Capitulation
        if bp0 >= 80 and v0 >= (v_mean * self.vol_mult):
            observations.append("Retail Panic Capitulation Discharge" if not is_bull else "High-Conviction Institutional Breakout Aggression")
            
        # 3-4. Rejection Blocks & Institutional Absorption Grid
        if lw0 >= 50 and c0 >= (l0 + spread0 * 0.35):
            observations.append("Aggressive Bullish Liquidity Sweep at Lows")
            if v0 >= (v_mean * 1.6): observations.append("Institutional Order Book Block Absorption")
        if uw0 >= 50 and c0 <= (h0 - spread0 * 0.35):
            observations.append("Aggressive Bearish Liquidity Sweep at Highs")
            if v0 >= (v_mean * 1.6): observations.append("Institutional Distribution Supply Squeezing")
                
        # 5-6. Climax Clashes & Retail Trap Depths
        if v0 >= (v_mean * 2.2) and bp0 <= 15:
            observations.append("High-Volume Exhaustion Node")
            observations.append("Buyer-Seller Final Equilibrium Hand-off")
            
        # 7-8. Stop-Loss Hunting Loops (Retail Trapped States)
        if h0 > h1 and c0 < o0 and c0 < c1:
            observations.append("Bull Trap Induced / Retail Breakout Long Liquidation")
        if l0 < l1 and c0 > o0 and c0 > c1:
            observations.append("Bear Trap Induced / Retail Breakdown Short Squeezing")
            
        return {
            "engine": "candle_psychology_engine",
            "status": "BEHAVIORAL_METRICS_LOCKED",
            "raw_observations": observations
        }
