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

            return ticker.history(
                period=period,
                auto_adjust=False
            )

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

            info = ticker.info
            fast = ticker.fast_info

            roe = info.get("returnOnEquity")
            if roe is not None:
                roe *= 100

            roce = info.get("returnOnAssets")
            if roce is not None:
                roce *= 100

            sales_growth = info.get("revenueGrowth")
            if sales_growth is not None:
                sales_growth *= 100

            profit_growth = info.get("earningsGrowth")
            if profit_growth is not None:
                profit_growth *= 100

            operating_margin = info.get("operatingMargins")
            if operating_margin is not None:
                operating_margin *= 100

            net_margin = info.get("profitMargins")
            if net_margin is not None:
                net_margin *= 100

            dividend_yield = info.get("dividendYield")
            if dividend_yield is not None:
                dividend_yield *= 100

            debt_equity = info.get("debtToEquity")

            if debt_equity is not None:

                if debt_equity > 10:
                    debt_equity = debt_equity / 100

            promoter = info.get(
                "heldPercentInsiders"
            )

            if promoter is not None:
                promoter *= 100

            institutional = info.get(
                "heldPercentInstitutions"
            )

            if institutional is not None:
                institutional *= 100

            return {

                "symbol":
                    symbol,

                "market_cap":
                    fast.get("marketCap"),

                "week52_high":
                    fast.get("yearHigh"),

                "week52_low":
                    fast.get("yearLow"),

                "shares_outstanding":
                    fast.get("shares"),

                "current_price":
                    fast.get("lastPrice"),

                "pe":
                    info.get("trailingPE"),

                "pb":
                    info.get("priceToBook"),

                "roe":
                    roe,

                "roce":
                    roce,

                "debt_equity":
                    debt_equity,

                "dividend_yield":
                    dividend_yield,

                "beta":
                    info.get("beta"),

                "eps":
                    info.get("trailingEps"),

                "book_value":
                    info.get("bookValue"),

                "sector":
                    info.get("sector"),

                "industry":
                    info.get("industry"),

                "cash":
                    info.get("totalCash"),

                "free_cash_flow":
                    info.get("freeCashflow"),

                "enterprise_value":
                    info.get("enterpriseValue"),

                "target_price":
                    info.get("targetMeanPrice"),

                "recommendation":
                    info.get("recommendationKey"),

                "current_ratio":
                    info.get("currentRatio"),

                "quick_ratio":
                    info.get("quickRatio"),

                "operating_margin":
                    operating_margin,

                "net_margin":
                    net_margin,

                "sales_growth":
                    sales_growth,

                "profit_growth":
                    profit_growth,

                "promoter_holding":
                    promoter,

                "institutional_holding":
                    institutional,

                "fii_holding":
                    institutional,

                "dii_holding":
                    None

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

        if income is None or income.empty:
            return rows

        for col in income.columns:

            rows.append({

                "symbol":
                    symbol,

                "year":
                    str(col.date()),

                "revenue":
                    income.loc["Total Revenue", col]
                    if "Total Revenue" in income.index
                    else None,

                "net_income":
                    income.loc["Net Income", col]
                    if "Net Income" in income.index
                    else None,

                "total_assets":
                    balance.loc["Total Assets", col]
                    if balance is not None
                    and "Total Assets" in balance.index
                    else None,

                "total_debt":
                    balance.loc["Total Debt", col]
                    if balance is not None
                    and "Total Debt" in balance.index
                    else None,

                "operating_cf":
                    cashflow.loc["Operating Cash Flow", col]
                    if cashflow is not None
                    and "Operating Cash Flow" in cashflow.index
                    else None,

                "free_cf":
                    cashflow.loc["Free Cash Flow", col]
                    if cashflow is not None
                    and "Free Cash Flow" in cashflow.index
                    else None

            })

        return rows
