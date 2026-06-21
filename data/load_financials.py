from providers.yahoo_provider import YahooProvider
from core.db import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS financials (
        symbol TEXT,
        year TEXT,

        revenue REAL,
        gross_profit REAL,
        operating_income REAL,
        net_income REAL,

        eps REAL,

        total_assets REAL,
        total_liabilities REAL,
        shareholders_equity REAL,

        cash REAL,
        debt REAL,

        operating_cashflow REAL,
        free_cashflow REAL,

        PRIMARY KEY(symbol, year)
    )
    """)

    conn.commit()
    conn.close()


def save_financials(symbol, rows):

    conn = get_connection()
    cur = conn.cursor()

    for row in rows:

        cur.execute("""
        INSERT OR REPLACE INTO financials
        (
            symbol,
            year,

            revenue,
            gross_profit,
            operating_income,
            net_income,

            eps,

            total_assets,
            total_liabilities,
            shareholders_equity,

            cash,
            debt,

            operating_cashflow,
            free_cashflow
        )
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            symbol,
            row["year"],

            row["revenue"],
            row["gross_profit"],
            row["operating_income"],
            row["net_income"],

            row["eps"],

            row["total_assets"],
            row["total_liabilities"],
            row["shareholders_equity"],

            row["cash"],
            row["debt"],

            row["operating_cashflow"],
            row["free_cashflow"]
        ))

    conn.commit()
    conn.close()


def load_symbol(symbol):

    provider = YahooProvider()

    rows = provider.get_financials(symbol)

    if len(rows) > 0:
        save_financials(symbol, rows)

    print(f"{symbol} financial saved")


def main():

    create_table()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT symbol FROM stock_master")

    symbols = [r[0] for r in cur.fetchall()]

    conn.close()

    total = len(symbols)

    print(f"Found {total} symbols")

    for i, symbol in enumerate(symbols, start=1):

        try:
            load_symbol(symbol)

            if i % 50 == 0:
                print(f"{i}/{total} completed")

        except Exception as e:
            print(symbol, e)


if __name__ == "__main__":
    main()
