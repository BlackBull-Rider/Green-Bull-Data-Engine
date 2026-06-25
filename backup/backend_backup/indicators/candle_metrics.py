import numpy as np
from typing import Dict
from backend.indicators.math_utils import enforce_writeable_float_array_fast

def compute_candlestick_raw_vectors(open_v: np.ndarray, high_v: np.ndarray, low_v: np.ndarray, close_v: np.ndarray) -> Dict[str, np.ndarray]:
    """
    [Green Bull Rider V6 - Layer 1: candle_metrics]
    Vectorizes raw geometric candle footprints over the entire historical block.
    """
    opens = enforce_writeable_float_array_fast(open_v)
    highs = enforce_writeable_float_array_fast(high_v)
    lows = enforce_writeable_float_array_fast(low_v)
    closes = enforce_writeable_float_array_fast(close_v)
    
    spreads = highs - lows
    safe_spreads = np.where(spreads == 0, 1e-7, spreads)
    
    bodies = np.abs(closes - opens)
    upper_wicks = highs - np.maximum(opens, closes)
    lower_wicks = np.minimum(opens, closes) - lows
    
    body_percentages = (bodies / safe_spreads) * 100.0
    upper_wick_percentages = (upper_wicks / safe_spreads) * 100.0
    lower_wick_percentages = (lower_wicks / safe_spreads) * 100.0
    
    return {
        "spreads": spreads,
        "bodies": bodies,
        "body_percentages": body_percentages,
        "upper_wick_percentages": upper_wick_percentages,
        "lower_wick_percentages": lower_wick_percentages
    }
