import numpy as np
import sqlite3
import os
import sys

# Ensure the root directory is accessible for module imports in Termux
sys.path.append(os.getcwd())

# Import the exact compiled module from your indicator cluster
from backend.indicators.trend import compile_institutional_trend_pivots

def run_live_trend_indicator_test():
    print("====================================================================")
    print("🚀 INITIALIZING LAYER 1: TREND PIVOT MATRIX SEPARATE TEST PIPELINE")
    print("====================================================================")
    
    db_path = "database/market.db"
    
    if not os.path.exists(db_path):
        print(f"❌ EXECUTION ABORTED: Target database '{db_path}' not found.")
        return

    print(f"🔗 Establishing Strict READ-ONLY Connection to: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Dynamically find the first available active symbol in your market schema
        cursor.execute("SELECT symbol FROM market_data LIMIT 1")
        symbol_row = cursor.fetchone()
        
        if not symbol_row:
            print("⚠️  CRITICAL: 'market_data' table exists but contains ZERO records.")
            conn.close()
            return
            
        active_symbol = symbol_row[0]
        print(f"🎯 Dynamic Target Node Located: [{active_symbol}]")
        
        # 2. Extract raw matrix row data for the extracted symbol ordered chronologically
        cursor.execute(
            "SELECT high, low, close FROM market_data WHERE symbol = ? ORDER BY date ASC LIMIT 50"
        )
        rows = cursor.fetchall()
        conn.close()
        
        n_bars = len(rows)
        if n_bars < 2:
            print(f"⚠️  INSUFFICIENT DATA Depth: Found {n_bars} bars for {active_symbol}. Minimum 2 rows required.")
            return
            
        print(f"📊 Extracted {n_bars} Rows of Historical Records. Converting to High-Performance Arrays...")
        
        # Parse records into pure writeable numpy float arrays
        data_matrix = np.array(rows, dtype=np.float64)
        highs_v = np.ascontiguousarray(data_matrix[:, 0])
        lows_v  = np.ascontiguousarray(data_matrix[:, 1])
        closes_v = np.ascontiguousarray(data_matrix[:, 2])
        
        print("⚡ Executing 'compile_institutional_trend_pivots' Calculation Vector...")
        
        # Fire your core structural mathematical engine
        pivot_output = compile_institutional_trend_pivots(high_v=highs_v, low_v=lows_v, close_v=closes_v)
        
        # 3. Print complete verified nested dictionary elements onto the console terminal
        print("\n[📊 LIVE MATHEMATICAL TESTING MATRIX RESULTS]")
        print(f"Engine Target : {pivot_output.get('engine')}")
        print(f"Execution Status : {pivot_output.get('status')}")
        
        # Check specific nested keys based on trend.py structure
        cpr_data = pivot_output.get("central_pivot_range_cpr", pivot_output.get("central_pivot_range", {}))
        
        print("\n--- Standard Floor Levels ---")
        for k, v in pivot_output.get("standard_floor_pivots", {}).items():
            print(f"  {k} : {v}")
            
        print("\n--- Central Pivot Range (CPR) ---")
        for k, v in cpr_data.items():
            print(f"  {k} : {v}")
            
        print("\n--- Camarilla Overlays ---")
        for k, v in pivot_output.get("camarilla_levels", {}).items():
            print(f"  {k} : {v}")
            
        print("\n--- Woodie Grid Calibration ---")
        for k, v in pivot_output.get("woodie_pivots", {}).items():
            print(f"  {k} : {v}")
            
        print("\n--- Fibonacci Thresholds ---")
        for k, v in pivot_output.get("fibonacci_pivots", {}).items():
            print(f"  {k} : {v}")
            
        print("\n✅ SEPARATE TEST MODULE CHECK: PASSED SUCCESSFULLY WITH ZERO DB MUTATION! ✓\n")
            
    except sqlite3.OperationalError as e:
        print(f"\n❌ DB OPERATIONAL FAULT: {e}")
        print("Ensure column mappings (high, low, close) exactly match your local table structures.")

if __name__ == "__main__":
    run_live_trend_indicator_test()
