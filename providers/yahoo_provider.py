import yfinance as yf


class YahooProvider:

    def get_history(
        self,
        symbol,
        period="250d"
    ):

        try:

            ticker = yf.Ticker(
                f"{symbol}.NS"
            )

            df = ticker.history(
                period=period,
                auto_adjust=False
            )

            return df

        except Exception as e:

            print(
                f"{symbol} history error:",
                e
            )

            return None

    def get_fundamentals(
        self,
        symbol
    ):

        try:

            ticker = yf.Ticker(
                f"{symbol}.NS"
            )

            info = ticker.fast_info

            return {

                "symbol": symbol,

                "market_cap":
                    info.get("marketCap"),

                "week52_high":
                    info.get("yearHigh"),

                "week52_low":
                    info.get("yearLow"),

                "shares_outstanding":
                    info.get("shares"),

                "current_price":
                    info.get("lastPrice")

            }

        except Exception as e:

            print(
                f"{symbol} fundamental error:",
                e
            )

            return {}

    def get_listing_date(
        self,
        symbol
    ):

        try:

            ticker = yf.Ticker(
                f"{symbol}.NS"
            )

            df = ticker.history(
                period="max"
            )

            if len(df) == 0:
                return None

            return str(
                df.index[0].date()
            )

        except Exception:

            return None

    def get_financials(
        self,
        symbol
    ):

        ticker = yf.Ticker(
            f"{symbol}.NS"
        )

        rows = []

        try:
            income = ticker.financials
        except:
            income = None

        try:
            balance = ticker.balance_sheet
        except:
            balance = None

        try:
            cashflow = ticker.cashflow
        except:
            cashflow = None

        if (
            income is None
            or income.empty
        ):
            return rows

        for col in income.columns:

            revenue = None
            net_income = None
            total_assets = None
            total_debt = None
            operating_cf = None
            free_cf = None

            try:
                revenue = income.loc[
                    "Total Revenue",
                    col
                ]
            except:
                pass

            try:
                net_income = income.loc[
                    "Net Income",
                    col
                ]
            except:
                pass

            try:
                total_assets = balance.loc[
                    "Total Assets",
                    col
                ]
            except:
                pass

            try:
                total_debt = balance.loc[
                    "Total Debt",
                    col
                ]
            except:
                pass

            try:
                operating_cf = cashflow.loc[
                    "Operating Cash Flow",
                    col
                ]
            except:
                pass

            try:
                free_cf = cashflow.loc[
                    "Free Cash Flow",
                    col
                ]
            except:
                pass

            rows.append({

                "symbol":
                    symbol,

                "year":
                    str(col.date()),

                "revenue":
                    revenue,

                "net_income":
                    net_income,

                "total_assets":
                    total_assets,

                "total_debt":
                    total_debt,

                "operating_cf":
                    operating_cf,

                "free_cf":
                    free_cf
            })

        return rows
