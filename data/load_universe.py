import pandas as pd
from core.db import get_connection

df = pd.read_csv("https://archives.nseindia.com/content/equities/EQUITY_L.csv")

df = df.rename(columns={
    "SYMBOL": "symbol",
    "NAME OF COMPANY": "company_name"
})

df = df[["symbol", "company_name"]]
df["exchange"] = "NSE"

conn = get_connection()

df.to_sql(
    "stock_master",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Loaded:", len(df), "stocks")
