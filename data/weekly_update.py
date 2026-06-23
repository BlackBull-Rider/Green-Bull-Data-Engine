from data.load_universe import main as universe_sync
from data.load_fundamentals import main as fundamentals_sync
from data.load_ipo import main as ipo_sync


def main():

    print("\nUNIVERSE UPDATE")
    universe_sync()

    print("\nFUNDAMENTALS UPDATE")
    fundamentals_sync()

    print("\nIPO UPDATE")
    ipo_sync()

    print("\nWEEKLY UPDATE COMPLETED")


if __name__ == "__main__":
    main()
