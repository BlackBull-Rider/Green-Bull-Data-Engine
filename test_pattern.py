import numpy as np
import sqlite3
import os
import json
from backend.engines.candle_pattern_engine import CandlePatternEngine

def run_pattern_engine_test():
    db_path = "database/market.db"
    
    if not os.path.exists(db_path):
        error_payload = {
            "candle_pattern_engine": "v1.1",
            "status": "FAILED_DATABASE_NOT_FOUND",
            "active_patterns_detected": []
        }
        print(json.dumps(error_payload, indent=4))
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Strictly query historical data rows for RELIANCE to keep data audit seamless
        target_symbol = "RELIANCE"
        cursor.execute(
            "SELECT open, high, low, close, volume FROM historical_data WHERE symbol = ? ORDER BY date ASC LIMIT 100",
            (target_symbol,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        if len(rows) < 5:
            error_payload = {
                "candle_pattern_engine": "v1.1",
                "status": f"FAILED_INSUFFICIENT_ROWS_FOR_{target_symbol}",
                "active_patterns_detected": []
            }
            print(json.dumps(error_payload, indent=4))
            return
            
        # Parse arrays into pure contiguous float64 arrays
        data = np.array(rows, dtype=np.float64)
        opens, highs, lows, closes, volumes = data[:, 0], data[:, 1], data[:, 2], data[:, 3], data[:, 4]
        
        # Instantiate and execute Engine
        engine = CandlePatternEngine()
        output_payload = engine.evaluate_pattern_intelligence(opens, highs, lows, closes, volumes)
        
        # Inject test target context into output payload for clear tracking
        output_payload["test_target_node"] = target_symbol
        
        # Output strictly clean, indented JSON string directly onto terminal screen
        print(json.dumps(output_payload, indent=4))
        
    except Exception as e:
        fault_payload = {
            "candle_pattern_engine": "v1.1",
            "status": "CRITICAL_EXCEPTION_RAISED",
            "error_details": str(e)
        }
        print(json.dumps(fault_payload, indent=4))

if __name__ == "__main__":
    run_pattern_engine_test()
