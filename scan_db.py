import sqlite3
import pandas as pd

# তোর ডাটাবেসের সাথে কানেক্ট করা
conn = sqlite3.connect("market.db")

# ডাটাবেসে কী কী টেবিল আছে সেটা বের করা
print("\n[+] Tables in database:")
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)

# প্রতিটা টেবিলের কলামের নাম এবং ডেটা টাইপ বের করা
for table in tables['name']:
    print(f"\n--- Columns for table: {table} ---")
    schema = pd.read_sql_query(f"PRAGMA table_info({table});", conn)
    print(schema[['name', 'type']])
    
conn.close()
