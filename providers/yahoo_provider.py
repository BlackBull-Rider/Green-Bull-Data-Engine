import yfinance as yf


class YahooProvider:

    def get_history(
        self,
        symbol,
        period="5y"
    ):

        ticker = yf.Ticker(
            f"{symbol}.NS"
        )

        df = ticker.history(
            period=period,
            auto_adjust=False
        )

        return df
