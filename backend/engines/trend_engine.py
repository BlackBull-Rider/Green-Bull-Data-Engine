import numpy as np
from typing import Dict, Any

class trend_engine:
    """
    [Green Bull Rider V6 - Engine 5: trend_engine]
    Production-Grade Trend Classifier. 100% Observation-Only.
    Decodes macro/micro trend velocities, DMI vector conflicts, and angular momentum at index -1.
    """
    def __init__(self, adx_threshold: float = 25.0, hyper_velocity_threshold: float = 40.0) -> None:
        self.adx_th = adx_threshold
        self.hyper_th = hyper_velocity_threshold

    def evaluate_trend_velocity(
        self, regression_slope: float, trend_angle_degrees: float, plus_di: float, minus_di: float, adx_strength: float
    ) -> Dict[str, Any]:
        
        observations = []
        
        # 1. Structural Trend Intensity Analysis via ADX
        is_trending = adx_strength >= self.adx_th
        if is_trending:
            if adx_strength >= self.hyper_th:
                observations.append("Hyper-Extended Institutional Momentum Velocity")
            else:
                observations.append("Strong Directional Trend Expansion Phase")
        else:
            observations.append("Weak Directional Grid / Sideways Non-Trending Consolidation")
            
        # 2. DMI Vector Conflict & Order Flow Alignment
        if plus_di > minus_di:
            observations.append("DMI Vector Dominated by Buyers (+DI Leading)")
            if is_trending and regression_slope > 0:
                observations.append("Confirmed Institutional Markup Sequence")
        elif minus_di > plus_di:
            observations.append("DMI Vector Dominated by Sellers (-DI Leading)")
            if is_trending and regression_slope < 0:
                observations.append("Confirmed Institutional Markdown Sequence")
        else:
            observations.append("DMI Vectors Interlocked / Complete Order Flow Equilibrium")
            
        # 3. Mathematical Angular Acceleration Profile
        abs_angle = abs(trend_angle_degrees)
        if abs_angle >= 55.0:
            observations.append("Parabolic Angular Acceleration (High Liquidation Risk)")
        elif abs_angle >= 35.0:
            observations.append("Healthy Structural Trend Incline Angle")
        elif abs_angle <= 12.0:
            observations.append("Flat Angular Exhaustion Zone / Imminent Trend Transition")
            
        return {
            "engine": "trend_engine",
            "status": "TREND_VELOCITY_CALIBRATED",
            "vector_metrics": {
                "is_active_trend_state": is_trending,
                "directional_spread": float(round(abs(plus_di - minus_di), 2))
            },
            "raw_observations": observations
        }
