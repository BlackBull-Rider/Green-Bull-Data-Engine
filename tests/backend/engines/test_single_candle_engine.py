cat << 'EOF' > tests/backend/engines/test_single_candle_engine.py
import numpy as np
from backend.engines.single_candle_engine import SingleCandleEngine

def test_single_candle_engine_marubozu_and_momentum():
    """
    Production test to validate institutional Marubozu and Momentum drive patterns.
    """
    opens = np.ones(20) * 100.0
    highs = np.ones(20) * 105.0
    lows = np.ones(20) * 95.0
    closes = np.ones(20) * 104.0
    volumes = np.ones(20) * 1000.0
    
    opens[-1] = 100.0
    highs[-1] = 110.0
    lows[-1] = 100.0
    closes[-1] = 110.0
    volumes[-1] = 2500.0  
    
    body_pct = np.ones(20) * 40.0
    body_pct[-1] = 100.0  
    upper_wick_pct = np.zeros(20)
    lower_wick_pct = np.zeros(20)
    atr = np.ones(20) * 5.0
    
    engine = SingleCandleEngine(atr_multiplier=1.5, volume_multiplier=1.5)
    result = engine.analyze_candle_mechanics(
        open_v=opens,
        high_v=highs,
        low_v=lows,
        close_v=closes,
        volume_v=volumes,
        body_pct_v=body_pct,
        upper_wick_pct_v=upper_wick_pct,
        lower_wick_pct_v=lower_wick_pct,
        atr_v=atr
    )
    
    assert result["engine"] == "single_candle_engine"
    assert "Bullish Marubozu" in result["raw_observations"]
    assert "Institutional Momentum Drive" in result["raw_observations"]
    assert result["metrics"]["body_percentage"] == 100.0
EOF
