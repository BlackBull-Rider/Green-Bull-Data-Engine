import numpy as np
import sqlite3
import os
import json
from backend.engines.single_candle_engine import SingleCandleEngine

def run_isolated_engine_test():
    db_path = "database/market.db"
    
    if not os.path.exists(db_path):
        error_payload = {
            "single_candle_engine": "v1.1",
            "status": "FAILED_DATABASE_NOT_FOUND",
            "active_candles_detected": [],
            "current_candle_metrics": {}
        }
        print(json.dumps(error_payload, indent=4))
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Strictly query historical data rows for RELIANCE to make tests instantly recognizable
        target_symbol = "RELIANCE"
        cursor.execute(
            "SELECT open, high, low, close, volume FROM historical_data WHERE symbol = ? ORDER BY date ASC LIMIT 100",
            (target_symbol,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        if len(rows) < 20:
            error_payload = {
                "single_candle_engine": "v1.1",
                "status": f"FAILED_INSUFFICIENT_ROWS_FOR_{target_symbol}",
                "active_candles_detected": [],
                "current_candle_metrics": {}
            }
            print(json.dumps(error_payload, indent=4))
            return
            
        # Parse arrays into contiguous numpy matrix
        data = np.array(rows, dtype=np.float64)
        opens, highs, lows, closes, volumes = data[:, 0], data[:, 1], data[:, 2], data[:, 3], data[:, 4]
        
        # Proxy Layer 1 ATR vector mapping
        atr_v = np.zeros_like(closes)
        atr_v[:] = np.mean(highs - lows)
        
        # Instantiate and execute Core Engine
        engine = SingleCandleEngine()
        output_payload = engine.analyze_candle_mechanics(opens, highs, lows, closes, volumes, atr_v)
        
        # Inject test target context into output payload for clear tracking
        output_payload["test_target_node"] = target_symbol
        
        # Strictly emit the audited clean JSON payload
        print(json.dumps(output_payload, indent=4))
        
    except Exception as e:
        fault_payload = {
            "single_candle_engine": "v1.1",
            "status": "CRITICAL_EXCEPTION_RAISED",
            "error_details": str(e)
        }
        print(json.dumps(fault_payload, indent=4))

if __name__ == "__main__":
    run_isolated_engine_test()
