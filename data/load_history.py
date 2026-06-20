from providers.yahoo_provider import YahooProvider
from core.db import get_connection

def save_history(symbol, df):
    conn = get_connection()
    cur = conn.cursor()

    for date, row in df.iterrows():
        cur.execute("""
        INSERT OR REPLACE INTO historical_data
        (
            symbol,
            date,
            open,
            high,
            low,
            close,
            volume
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            symbol,
            str(date.date()),
            float(row["Open"]),
            float(row["High"]),
            float(row["Low"]),
            float(row["Close"]),
            float(row["Volume"])
        ))

    conn.commit()
    conn.close()

def load_symbol(symbol):
    provider = YahooProvider()

    df = provider.get_history(symbol)

    save_history(symbol, df)

    print(f"{symbol} saved : {len(df)} rows")

def main():

    symbols = [
        "RELIANCE",
        "TCS",
        "INFY",
        "HDFCBANK",
        "ICICIBANK",
        "SBIN"
    ]

    for symbol in symbols:
        try:
            load_symbol(symbol)
        except Exception as e:
            print(symbol, e)

if __name__ == "__main__":
    main()
