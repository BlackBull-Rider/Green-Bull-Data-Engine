from providers.yahoo_provider import YahooProvider
from core.db import get_connection

from datetime import datetime


def save_fundamental(data):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO fundamental_data
        (
            symbol,
            market_cap,
            pe,
            pb,
            roe,
            roce,
            debt_equity,
            eps,
            book_value,
            dividend_yield,
            sector,
            industry,
            current_ratio,
            quick_ratio,
            operating_margin,
            net_margin,
            cash,
            free_cash_flow,
            enterprise_value,
            beta,
            week52_high,
            week52_low,
            target_price,
            recommendation,
            shares_outstanding,
            updated_at
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?,?,?,?,?,
            ?,?,?,?,?,?
        )
        """,
        (
            data["symbol"],
            data["market_cap"],
            data["pe"],
            data["pb"],
            data["roe"],
            data["roce"],
            data["debt_equity"],
            data["eps"],
            data["book_value"],
            data["dividend_yield"],
            data["sector"],
            data["industry"],
            data["current_ratio"],
            data["quick_ratio"],
            data["operating_margin"],
            data["net_margin"],
            data["cash"],
            data["free_cash_flow"],
            data["enterprise_value"],
            data["beta"],
            data["week52_high"],
            data["week52_low"],
            data["target_price"],
            data["recommendation"],
            data["shares_outstanding"],
            datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()


def main():

    provider = YahooProvider()

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

            data = provider.get_fundamentals(symbol)

            save_fundamental(data)

            print(symbol, "saved")

        except Exception as e:

            print(symbol, e)


if __name__ == "__main__":
    main()
