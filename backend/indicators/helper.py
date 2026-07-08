import sqlite3
import pandas as pd
import numpy as np
from backend.indicators.math_utils import enforce_writeable_float_array_fast

DB_PATH = "market.db"

def fetch_latest_market_data(symbol: str, limit: int = 1000) -> pd.DataFrame:
    """
    market.db থেকে নির্দিষ্ট সিম্বলের ডাটা ফেচ করার ফাংশন।
    লজিক: কোনো ফিক্সড রো থেকে নয়, বরং ORDER BY date DESC করে 
    সর্বশেষ (Latest) ডেটের এন্ট্রি থেকে ডাটা ফেচ করা হয়।
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        # লেটেস্ট ডেটা আগে পাওয়ার জন্য DESC ব্যবহার করা হলো
        query = f"SELECT * FROM ohlcv WHERE symbol = ? ORDER BY date DESC LIMIT ?"
        df = pd.read_sql_query(query, conn, params=(symbol, limit))
        conn.close()
        
        if df.empty:
            return pd.DataFrame()
            
        # ভেক্টর ক্যালকুলেশনের জন্য টাইম-সিরিজ সোজা (পুরনো থেকে নতুন) করে নেওয়া
        df = df.sort_values(by="date").reset_index(drop=True)
        return df
    except Exception as e:
        # প্রোডাকশন লেভেল এরর হ্যান্ডলিং
        print(f"[Database Warning]: {e}")
        return pd.DataFrame()

def get_entry_signal_data(df: pd.DataFrame) -> dict:
    """
    স্ক্রিনার সিগন্যাল লজিক: 
    AH কলামের (Buy/Sell Signal) সিগন্যাল দেখে B কলামের (Close Price) 
    ভ্যালুকে সরাসরি এন্ট্রি প্রাইস (Entry Price) হিসেবে এক্সট্র্যাক্ট করা।
    """
    if df.empty or 'close' not in df.columns or 'signal' not in df.columns:
        return {"date": None, "signal": None, "entry_price": 0.0}
        
    # রুল অনুযায়ী একদম সর্বশেষ (Latest) রো থেকে ডেটা নেওয়া হচ্ছে
    latest_row = df.iloc[-1]
    
    # AH কলাম লজিক: সিগন্যাল ফেচ করা
    current_signal = latest_row['signal'] 
    
    # B কলাম লজিক: Close price কেই Entry price হিসেবে ধরা হচ্ছে
    # (fast memory pointer use kore)
    close_array = enforce_writeable_float_array_fast(df['close'].values)
    entry_price = close_array[-1]
    
    return {
        "date": latest_row['date'],
        "signal": current_signal,
        "entry_price": float(entry_price)  # B কলাম (Close) = Entry
    }
