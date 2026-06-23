from datetime import datetime
from core.db import get_connection

from data.sync_history import main as history_sync
from data.load_indicators import main as indicators_sync
from data.update_latest_indicators import main as latest_sync
from data.load_fundamentals import main as fundamentals_sync
from data.load_ipo import main as ipo_sync


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


def run_step(name, func):

    try:

        print("\n" + "=" * 60)
        print(f"{name} STARTED")
        print("=" * 60)

        func()

        log_update(name.lower())

        print(f"{name} SUCCESS")

    except Exception as e:

        print(f"{name} FAILED")
        print(e)

        log_update(
            name.lower(),
            f"FAILED : {str(e)}"
        )

        raise


def main():

    if already_updated_today():

        print("Already Updated Today")
        return

    try:

        # 1. Latest OHLCV Update
        run_step(
            "HISTORY_SYNC",
            history_sync
        )

        # 2. Recalculate Indicators
        run_step(
            "INDICATORS",
            indicators_sync
        )

        # 3. Refresh Latest Indicators
        run_step(
            "LATEST_INDICATORS",
            latest_sync
        )

        # 4. Fundamentals
        run_step(
            "FUNDAMENTALS",
            fundamentals_sync
        )

        # 5. IPO Data
        run_step(
            "IPO",
            ipo_sync
        )

        log_update("daily_update")

        print("\nDAILY UPDATE COMPLETED")

    except Exception as e:

        print("\nDAILY UPDATE FAILED")
        print(e)

        log_update(
            "daily_update",
            f"FAILED : {str(e)}"
        )


if __name__ == "__main__":
    main()
