import numpy as np
from typing import Dict, Any

class support_resistance_engine:
    """
    [Green Bull Rider V6 - Engine 7: support_resistance_engine]
    Production-Grade Pivot Barrier Auditor. 100% Observation-Only.
    Tracks structural proximity alerts across 5 distinct institutional pivot configurations at index -1.
    """
    def __init__(self, proximity_limit_pct: float = 0.20) -> None:
        self.prox_lim = proximity_limit_pct # Proximity window (e.g. 0.20% from a key pivot level)

    def map_pivot_proximity(self, current_close: float, pivot_payload: Dict[str, Any]) -> Dict[str, Any]:
        observations = []
        
        if "standard_floor_pivots" not in pivot_payload or "central_pivot_range_cpr" not in pivot_payload:
            return {"engine": "support_resistance_engine", "status": "FAILED_SCHEMA_ERROR", "raw_observations": []}
            
        c_price = current_close
        
        # 1. CPR Envelopes Internal/External Scanning
        cpr = pivot_payload["central_pivot_range_cpr"]
        tc, pp, bc = float(cpr["TC"]), float(cpr["Pivot"]), float(cpr["BC"])
        
        if bc <= c_price <= tc:
            observations.append("Price Trading Locked Inside Central Pivot Range (CPR) Magnet Zone")
        elif c_price > tc:
            observations.append("Price Holding Structural Position Above Central CPR Line (Bullish S/R Support)")
        elif c_price < bc:
            observations.append("Price Holding Structural Position Below Central CPR Line (Bearish S/R Resistance)")
            
        # 2. Multi-Pivot Proximity Matcher (Standard Floors & Fibonacci)
        std_pivots = pivot_payload["standard_floor_pivots"]
        for level_name, level_val in std_pivots.items():
            dist_pct = (abs(c_price - float(level_val)) / float(level_val)) * 100.0
            if dist_pct <= self.prox_lim:
                observations.append(f"Price Proximity Critical Alert: Converging with Standard Floor {level_name}")
                
        fib_pivots = pivot_payload.get("fibonacci_pivots", {})
        for level_name, level_val in fib_pivots.items():
            dist_pct = (abs(c_price - float(level_val)) / float(level_val)) * 100.0
            if dist_pct <= self.prox_lim:
                observations.append(f"Price Proximity Critical Alert: Converging with Fibonacci {level_name} Level")
                
        # 3. Camarilla Extreme Expansion Barriers Tracking
        cam = pivot_payload["camarilla_levels"]
        r4, r3, s3, s4 = float(cam["R4"]), float(cam["R3"]), float(cam["S3"]), float(cam["S4"])
        
        if c_price >= r4:
            observations.append("Camarilla R4 Breakout Horizon Pierced (Trend Expansion Mode Triggered)")
        elif c_price <= s4:
            observations.append("Camarilla S4 Breakdown Horizon Pierced (Trend Expansion Mode Triggered)")
        elif r3 >= c_price >= s3:
            observations.append("Price Interlocked inside Camarilla Inner Compression Range Limits")
            
        return {
            "engine": "support_resistance_engine",
            "status": "PROXIMITY_BARRIERS_MAPPED",
            "raw_observations": observations
        }
