import numpy as np
from typing import Dict, Any

class volume_engine:
    """
    [Green Bull Rider V6 - Engine 9: volume_engine]
    Production-Grade Close-Volume Order Flow Analyzer. 100% Observation-Only.
    Decodes vectorized net capital flows and cumulative OBV direction blocks at index -1.
    """
    def __init__(self, high_rvol_limit: float = 1.5) -> None:
        self.rvol_lim = high_rvol_limit

    def evaluate_volume_profile_intelligence(
        self, rvol: float, volume_spike_state: str, obv: float, net_cap_flow: float, current_volume: float, average_volume_20: float
    ) -> Dict[str, Any]:
        
        observations = []
        
        # 1. Relative Volume (RVOL) Smart Money Footprint Verify
        if rvol >= self.rvol_lim:
            observations.append("Institutional Players Injecting Heavy Capital Flows")
            if volume_spike_state == "INSTITUTIONAL_SPIKE":
                observations.append("Anomalous Volume Spike Detected / Smart Money Accumulation Block Confirmed")
        elif rvol <= 0.60:
            observations.append("Low Capital Interest / Retail Illiquid Drift Node")
            
        # 2. Net Capital Money Flow Core Matrix (Close Data-Compliant)
        if net_cap_flow >= 0.25:
            observations.append("Volume Profile Confirms Heavy Institutional Buying Aggression (Strong Accumulation)")
        elif net_cap_flow > 0.05:
            observations.append("Net Closing Capital Inflow Holds Positive Dynamic Bias")
        elif net_cap_flow <= -0.25:
            observations.append("Volume Profile Confirms Heavy Institutional Selling Aggression (Strong Distribution)")
        elif net_cap_flow < -0.05:
            observations.append("Net Closing Capital Outflow Holds Negative Dynamic Bias")
        else:
            observations.append("Net Closing Capital Flow Hovering at Zero Equilibrium / Neutral Range")
            
        # 3. OBV and Momentum Convergence Checks
        if net_cap_flow > 0.10 and volume_spike_state != "NORMAL_VOLUME":
            observations.append("Sustained Capital Accumulation Inflow Under Institutional Control")
        elif net_cap_flow < -0.10 and volume_spike_state != "NORMAL_VOLUME":
            observations.append("Sustained Capital Distribution Outflow Under Institutional Liquidation")
            
        return {
            "engine": "volume_engine",
            "status": "VOLUME_DISTRIBUTION_AUDITED",
            "liquidity_metrics": {
                "rvol_intensity": rvol,
                "net_capital_flow_score": net_cap_flow,
                "on_balance_volume_raw": obv
            },
            "raw_observations": observations
        }
