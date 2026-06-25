import sqlite3
import pandas as pd
import os

class DatabaseHelper:
    """
    [Core Infrastructure Pipeline - Locked Schema]
    Handles optimized raw OHLCV extraction from the local SQLite ledger.
    Strictly queries the verified 'historical_data' table ordered chronologically by 'date'.
    """
    def __init__(self, db_path: str = "database/market.db") -> None:
        self.db_path = db_path

    def fetch_historical_ohlcv(self, symbol: str) -> pd.DataFrame:
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Physical database layer broken. Missing at: {self.db_path}")
            
        conn = sqlite3.connect(self.db_path)
        # Querying the actual verified historical_data table
        query = """
            SELECT date, open, high, low, close, volume 
            FROM historical_data 
            WHERE symbol = ? 
            ORDER BY date ASC
        """
        try:
            df = pd.read_sql_query(query, conn, params=(symbol,))
            return df
        except Exception as e:
            raise RuntimeError(f"Database query error for token '{symbol}': {str(e)}")
        finally:
            conn.close()
