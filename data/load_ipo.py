from core.db import get_connection
import yfinance as yf
from datetime import datetime
import time


def save_ipo(data):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO ipo_data
        (
            symbol,
            listing_date,
            current_price,
            market_cap,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["symbol"],
            data["listing_date"],
            data["current_price"],
            data["market_cap"],
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()


def process_symbol(symbol):

    t = yf.Ticker(f"{symbol}.NS")

    hist = t.history(period="max")

    if hist.empty:
        return

    listing_date = str(hist.index[0].date())

    current_price = float(hist["Close"].iloc[-1])

    fi = t.fast_info

    market_cap = fi.get("marketCap")

    save_ipo({
        "symbol": symbol,
        "listing_date": listing_date,
        "current_price": current_price,
        "market_cap": market_cap
    })

    print(symbol, listing_date)


def main():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT symbol FROM stock_master")

    symbols = [x[0] for x in cur.fetchall()]

    conn.close()

    print("TOTAL:", len(symbols))

    for i, symbol in enumerate(symbols, 1):

        try:

            process_symbol(symbol)

            if i % 50 == 0:
                print(f"{i}/{len(symbols)} completed")

            time.sleep(0.5)

        except Exception as e:

            print(symbol, e)


if __name__ == "__main__":
    main()
