import numpy as np
from typing import Dict, Any

class CandlePatternEngine:
    """
    [Green Bull Rider V6 - Layer 2: Engine 2]
    Production-Grade Multi-Candle Pattern Auditor. 100% Read-Only Architecture.
    Decodes exactly 12 structural sequence patterns using historical OHLCV matrices.
    """
    def __init__(self) -> None:
        pass

    def evaluate_pattern_intelligence(
        self, 
        open_v: np.ndarray, 
        high_v: np.ndarray, 
        low_v: np.ndarray, 
        close_v: np.ndarray,
        volume_v: np.ndarray
    ) -> Dict[str, Any]:
        
        n = close_v.shape[0]
        if n < 5:
            return {
                "candle_pattern_engine": "v1.0",
                "status": "FAILED_INSUFFICIENT_DEPTH",
                "active_patterns_detected": []
            }
            
        active_patterns = []
        
        # Pointers for index -1 (Current Active), -2 (Previous), and -3 (T-2 Node)
        c_o, c_h, c_l, c_c = float(open_v[-1]), float(high_v[-1]), float(low_v[-1]), float(close_v[-1])
        p_o, p_h, p_l, p_c = float(open_v[-2]), float(high_v[-2]), float(low_v[-2]), float(close_v[-2])
        p2_o, p2_h, p2_l, p2_c = float(open_v[-3]), float(high_v[-3]), float(low_v[-3]), float(close_v[-3])
        
        is_c_bull, is_c_bear = c_c > c_o, c_c < c_o
        is_p_bull, is_p_bear = p_c > p_o, p_c < p_o
        is_p2_bull, is_p2_bear = p2_c > p2_o, p2_c < p2_o
        
        body_c, body_p, body_p2 = abs(c_c - c_o), abs(p_c - p_o), abs(p2_c - p2_o)
        
        # 1-2. Bullish & Bearish Engulfing Suite
        if is_p_bear and is_c_bull and c_c >= p_o and c_o <= p_c and body_c > body_p:
            active_patterns.append({"type": "Bullish Engulfing", "strength": "High"})
        elif is_p_bull and is_c_bear and c_c <= p_o and c_o >= p_c and body_c > body_p:
            active_patterns.append({"type": "Bearish Engulfing", "strength": "High"})
            
        # 3. Harami Complex
        if c_h <= p_h and c_l >= p_l:
            if is_p_bear and is_c_bull and c_c <= p_o and c_o >= p_c:
                active_patterns.append({"type": "Harami", "setup": "Bullish Reversal"})
            elif is_p_bull and is_c_bear and c_c >= p_o and c_o <= p_c:
                active_patterns.append({"type": "Harami", "setup": "Bearish Distribution"})
                
        # 4-5. Morning & Evening Stars (3-Bar Structural Sequences)
        median_body = np.median(abs(close_v - open_v))
        if is_p2_bear and body_p2 > median_body * 0.7 and body_p < (body_p2 * 0.4) and min(p_o, p_c) < p2_c and is_c_bull and c_c > (p2_l + (body_p2 / 2.0)):
            active_patterns.append({"type": "Morning Star", "is_liquidity_sourced": True})
        if is_p2_bull and body_p2 > median_body * 0.7 and body_p < (body_p2 * 0.4) and max(p_o, p_c) > p2_c and is_c_bear and c_c < (p2_h - (body_p2 / 2.0)):
            active_patterns.append({"type": "Evening Star", "is_liquidity_sourced": True})
                    
        # 6-7. Three White Soldiers & Three Black Crows
        if is_p2_bull and is_p_bull and is_c_bull and c_c > p_c and p_c > p2_c:
            active_patterns.append({"type": "Three Soldiers"})
        elif is_p2_bear and is_p_bear and is_c_bear and c_c < p_c and p_c < p2_c:
            active_patterns.append({"type": "Three Crows"})
                
        # 8-9. Inside Bar & Outside Bar Coiling/Sweeps
        if c_h <= p_h and c_l >= p_l:
            active_patterns.append({"type": "Inside Bar", "mode": "Compression"})
        if c_h > p_h and c_l < p_l:
            active_patterns.append({"type": "Outside Bar", "mode": "Liquidity Sweep"})
            
        # 10-11. Piercing Line & Dark Cloud Cover
        p_midpoint = p_l + (body_p / 2.0)
        if is_p_bear and is_c_bull and c_o < p_l and c_c >= p_midpoint and c_c < p_o:
            active_patterns.append({"type": "Piercing"})
        elif is_p_bull and is_c_bear and c_o > p_h and c_c <= p_midpoint and c_c > p_o:
            active_patterns.append({"type": "Dark Cloud"})
            
        # 12. Tweezers (Precise high/low matching validation)
        toll = (c_h + p_h) * 0.0005
        if abs(c_h - p_h) <= toll and max(c_h, p_h) > max(open_v[-5:-2]):
            active_patterns.append({"type": "Tweezers", "formation": "Top"})
        elif abs(c_l - p_l) <= toll and min(c_l, p_l) < min(open_v[-5:-2]):
            active_patterns.append({"type": "Tweezers", "formation": "Bottom"})
            
        return {
            "candle_pattern_engine": "v1.1",
            "active_patterns_detected": active_patterns
        }
