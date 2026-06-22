data/daily_update.py

from datetime import datetime
from core.db import get_connection

from data.sync_history import main as history_sync
from data.update_latest_indicators import main as latest_sync

def log_update(process_name, status="SUCCESS"):

conn = get_connection()
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS update_log (
        process_name TEXT PRIMARY KEY,
        last_run TEXT,
        status TEXT
    )
    """
)

cur.execute(
    """
    INSERT OR REPLACE INTO update_log
    (
        process_name,
        last_run,
        status
    )
    VALUES (?, ?, ?)
    """,
    (
        process_name,
        datetime.now().isoformat(),
        status
    )
)

conn.commit()
conn.close()

def already_updated_today():

conn = get_connection()
cur = conn.cursor()

cur.execute(
    """
    SELECT last_run
    FROM update_log
    WHERE process_name='daily_update'
    """
)

row = cur.fetchone()

conn.close()

if row is None:
    return False

last_date = row[0][:10]
today = datetime.now().strftime("%Y-%m-%d")

return last_date == today

def main():

if already_updated_today():

    print("Already Updated Today")
    return

try:

    print("History Sync Started")
    history_sync()
    log_update("history_sync")

    print("Latest Indicator Refresh")
    latest_sync()
    log_update("latest_indicator_sync")

    log_update("daily_update")

    print("Daily Update Completed")

except Exception as e:

    print("Update Failed:", e)

    log_update(
        "daily_update",
        f"FAILED : {str(e)}"
    )

if name == "main":
main()
