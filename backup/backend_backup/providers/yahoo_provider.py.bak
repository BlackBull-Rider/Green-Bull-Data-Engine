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

    def get_fundamentals(
        self,
        symbol
    ):

        ticker = yf.Ticker(
            f"{symbol}.NS"
        )

        info = ticker.info

        return {
            "market_cap": info.get("marketCap"),
            "pe": info.get("trailingPE"),
            "pb": info.get("priceToBook"),
            "roe": info.get("returnOnEquity"),
            "dividend_yield": info.get("dividendYield"),
            "eps": info.get("trailingEps"),
            "book_value": info.get("bookValue")
        }
