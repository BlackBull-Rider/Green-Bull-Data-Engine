from providers.yahoo_provider import YahooProvider
from core.db import get_connection


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
            sales_growth,
            profit_growth,
            promoter_holding,
            institutional_holding,
            fii_holding,
            dii_holding,
            dividend_yield,
            sector,
            industry,
            eps,
            book_value,
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
            shares_outstanding
        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """,
        (
            data.get("symbol"),
            data.get("market_cap"),
            data.get("pe"),
            data.get("pb"),
            data.get("roe"),
            data.get("roce"),
            data.get("debt_equity"),
            data.get("sales_growth"),
            data.get("profit_growth"),
            data.get("promoter_holding"),
            data.get("institutional_holding"),
            data.get("fii_holding"),
            data.get("dii_holding"),
            data.get("dividend_yield"),
            data.get("sector"),
            data.get("industry"),
            data.get("eps"),
            data.get("book_value"),
            data.get("current_ratio"),
            data.get("quick_ratio"),
            data.get("operating_margin"),
            data.get("net_margin"),
            data.get("cash"),
            data.get("free_cash_flow"),
            data.get("enterprise_value"),
            data.get("beta"),
            data.get("week52_high"),
            data.get("week52_low"),
            data.get("target_price"),
            data.get("recommendation"),
            data.get("shares_outstanding")
        )
    )

    conn.commit()
    conn.close()


def load_symbol(symbol):

    provider = YahooProvider()

    data = provider.get_fundamentals(symbol)

    if not data:
        print(symbol, "no data")
        return

    data["symbol"] = symbol

    save_fundamental(data)

    print(symbol, "fundamental saved")


def main():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT symbol
        FROM stock_master
        ORDER BY symbol
        """
    )

    symbols = [row[0] for row in cur.fetchall()]

    conn.close()

    print(f"Found {len(symbols)} symbols")

    import time

    for i, symbol in enumerate(symbols, 1):

        try:

            load_symbol(symbol)

            if i % 50 == 0:
                print(f"{i}/{len(symbols)} completed")

            time.sleep(1)

        except Exception as e:

            print(symbol, e)


if __name__ == "__main__":
    main()
