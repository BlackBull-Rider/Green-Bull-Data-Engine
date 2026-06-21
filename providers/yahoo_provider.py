import yfinance as yf


class YahooProvider:

    def get_history(self, symbol, period="5y"):

        ticker = yf.Ticker(f"{symbol}.NS")

        df = ticker.history(
            period=period,
            auto_adjust=False
        )

        return df

    def get_fundamentals(self, symbol):

        ticker = yf.Ticker(f"{symbol}.NS")
        info = ticker.info

        return {
            "symbol": symbol,

            "market_cap": info.get("marketCap"),
            "pe": info.get("trailingPE"),
            "pb": info.get("priceToBook"),

            "roe": info.get("returnOnEquity"),
            "roce": info.get("returnOnAssets"),

            "debt_equity": info.get("debtToEquity"),

            "eps": info.get("trailingEps"),
            "book_value": info.get("bookValue"),

            "dividend_yield": info.get("dividendYield"),

            "sector": info.get("sector"),
            "industry": info.get("industry"),

            "current_ratio": info.get("currentRatio"),
            "quick_ratio": info.get("quickRatio"),

            "operating_margin": info.get("operatingMargins"),
            "net_margin": info.get("profitMargins"),

            "cash": info.get("totalCash"),

            "free_cash_flow": info.get("freeCashflow"),

            "enterprise_value": info.get("enterpriseValue"),

            "beta": info.get("beta"),

            "week52_high": info.get("fiftyTwoWeekHigh"),
            "week52_low": info.get("fiftyTwoWeekLow"),

            "target_price": info.get("targetMeanPrice"),

            "recommendation": info.get("recommendationKey"),

            "shares_outstanding": info.get("sharesOutstanding")
        }

    def get_financials(self, symbol):

        ticker = yf.Ticker(f"{symbol}.NS")

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

            revenue = None
            net_income = None
            total_assets = None
            total_debt = None
            operating_cf = None
            free_cf = None

            try:
                revenue = income.loc["Total Revenue", col]
            except:
                pass

            try:
                net_income = income.loc["Net Income", col]
            except:
                pass

            try:
                total_assets = balance.loc["Total Assets", col]
            except:
                pass

            try:
                total_debt = balance.loc["Total Debt", col]
            except:
                pass

            try:
                operating_cf = cashflow.loc["Operating Cash Flow", col]
            except:
                pass

            try:
                free_cf = cashflow.loc["Free Cash Flow", col]
            except:
                pass

            rows.append({
                "symbol": symbol,
                "year": str(col.date()),
                "revenue": revenue,
                "net_income": net_income,
                "total_assets": total_assets,
                "total_debt": total_debt,
                "operating_cf": operating_cf,
                "free_cf": free_cf
            })

        return rows
