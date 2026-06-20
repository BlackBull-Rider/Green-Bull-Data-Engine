from providers.yahoo_provider import YahooProvider

def main():
    provider = YahooProvider()

    df = provider.get_history("RELIANCE")

    print(df.head())
    print("Rows:", len(df))

if __name__ == "__main__":
    main()
