from datetime import datetime
from core.db import get_connection

from data.load_universe import main as universe_update
from data.sync_history import main as history_update
from data.load_fundamentals import main as fundamentals_update
from data.load_ipo import main as ipo_update
from data.update_latest_indicators import main as latest_update


def log_update(process):

    conn = get_connection()
    cur = conn.cursor()

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
            process,
            datetime.now().isoformat(),
            "SUCCESS"
        )
    )

    conn.commit()
    conn.close()


def run_process(name, func):

    try:

        print(f"\n{'=' * 50}")
        print(f"{name} STARTED")
        print(f"{'=' * 50}")

        func()

        log_update(name.lower())

        print(f"{name} SUCCESS")

    except Exception as e:

        print(f"{name} FAILED")
        print(e)


def main():

    run_process(
        "UNIVERSE",
        universe_update
    )

    run_process(
        "HISTORY",
        history_update
    )

    run_process(
        "FUNDAMENTALS",
        fundamentals_update
    )

    run_process(
        "IPO",
        ipo_update
    )

    run_process(
        "LATEST_INDICATORS",
        latest_update
    )

    print("\nDAILY UPDATE COMPLETED")


if __name__ == "__main__":
    main()
