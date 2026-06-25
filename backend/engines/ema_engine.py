import numpy as np
from typing import Dict, Any

class ema_engine:
    """
    [Green Bull Rider V6 - Engine 6: ema_engine]
    Production-Grade Mean Reversion & Baseline Tracker. 100% Observation-Only.
    Evaluates cross-confluence and dynamic pricing gaps across 5 institutional moving averages at index -1.
    """
    def __init__(self, high_gap_threshold_pct: float = 2.5) -> None:
        self.gap_th = high_gap_threshold_pct

    def evaluate_moving_average_intelligence(
        self, current_close: float, sma_20: float, ema_50: float, hull_ma_20: float, zero_lag_ema_20: float, kama_20: float
    ) -> Dict[str, Any]:
        
        observations = []
        c_price = current_close
        
        # 1. Macro Trend Alignment Filters (SMA 20 vs EMA 50)
        if c_price > sma_20 and sma_20 > ema_50:
            observations.append("Perfect Bullish Moving Average Alignment Sequence")
        elif c_price < sma_20 and sma_20 < ema_50:
            observations.append("Perfect Bearish Moving Average Alignment Sequence")
            
        # 2. Fast Velocity Leads (Hull MA vs Zero Lag EMA)
        if hull_ma_20 > zero_lag_ema_20:
            observations.append("Fast Hull Vector Leading Zero-Lag Momentum")
            if c_price > hull_ma_20:
                observations.append("Bullish Price Expansion Above High-Speed Medians")
        else:
            observations.append("Fast Hull Vector Lagging Zero-Lag Momentum")
            if c_price < hull_ma_20:
                observations.append("Bearish Price Expansion Below High-Speed Medians")
                
        # 3. Mean Overextension Matrix (Gap Analysis against Macro EMA 50)
        ema_gap_pct = ((c_price - ema_50) / ema_50) * 100.0
        if abs(ema_gap_pct) >= self.gap_th:
            if ema_gap_pct > 0:
                observations.append("Price Overextended Bullish Above Macro Mean / Mean Reversion Imminent")
            else:
                observations.append("Price Overextended Bearish Below Macro Mean / Mean Reversion Imminent")
                
        # 4. Adaptive Price Coiling (KAMA Coincidence Filter)
        kama_gap_pct = (abs(c_price - kama_20) / kama_20) * 100.0
        if kama_gap_pct <= 0.35:
            observations.append("Price Coiled inside Adaptive Kaufman Mean Equilibrium")
            
        return {
            "engine": "ema_engine",
            "status": "BASELINES_CONFLUENCE_MAPPED",
            "gap_metrics": {
                "macro_ema_gap_percentage": float(round(ema_gap_pct, 2)),
                "adaptive_kama_gap_percentage": float(round(kama_gap_pct, 3))
            },
            "raw_observations": observations
        }
