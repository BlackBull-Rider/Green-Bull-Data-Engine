"""
GREEN BULL DATA ENGINE

Enterprise Yahoo Finance Provider

Author : New AI Bull V1
Python : 3.13
"""

from __future__ import annotations

import logging
import time
from datetime import date, datetime
from typing import Any

import pandas as pd
import yfinance as yf

from backend.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class YahooProvider(BaseProvider):
    """
    Enterprise Yahoo Finance Provider.

    Responsibilities
    ----------------
    - Fetch Market History
    - Fetch Fundamentals
    - Fetch Financial Statements
    - Fetch Corporate Actions
    - Fetch Company Information

    This class NEVER writes into database.
    """

    MAX_RETRY = 3

    def __init__(self) -> None:

        self._ticker_cache: dict[str, yf.Ticker] = {}

    # =====================================================
    # Internal Helpers
    # =====================================================

    def _symbol(self, symbol: str) -> str:
        """
        Convert NSE symbol.
        """

        symbol = symbol.strip().upper()

        if symbol.endswith(".NS"):
            return symbol

        return f"{symbol}.NS"

    def _ticker(self, symbol: str) -> yf.Ticker:
        """
        Cached ticker object.
        """

        key = self._symbol(symbol)

        if key not in self._ticker_cache:
            self._ticker_cache[key] = yf.Ticker(key)

        return self._ticker_cache[key]

    def _retry(self, func, *args, **kwargs):

        last_error = None

        for attempt in range(1, self.MAX_RETRY + 1):

            try:
                return func(*args, **kwargs)

            except Exception as exc:

                last_error = exc

                logger.warning(
                    "Yahoo retry %s/%s failed : %s",
                    attempt,
                    self.MAX_RETRY,
                    exc,
                )

                time.sleep(attempt)

        raise last_error

    # =====================================================
    # Validators
    # =====================================================

    def validate_history(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:

        if df is None:
            return pd.DataFrame()

        if df.empty:
            return pd.DataFrame()

        df = df.copy()

        df.columns = [
            c.lower().replace(" ", "_")
            for c in df.columns
        ]

        required = [
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]

        for col in required:

            if col not in df.columns:
                raise ValueError(
                    f"Missing column : {col}"
                )

        df = df[
            [
                "open",
                "high",
                "low",
                "close",
                "volume",
            ]
        ]

        df = df.dropna()

        df = df[df["volume"] >= 0]

        df.index = pd.to_datetime(df.index)

        df = df.sort_index()

        df = df[~df.index.duplicated()]

        return df

    def _safe_info(
        self,
        ticker: yf.Ticker,
    ) -> dict[str, Any]:

        try:
            info = self._retry(
                lambda: ticker.info
            )

            if info is None:
                return {}

            return info

        except Exception as exc:

            logger.warning(
                "Unable to fetch company info : %s",
                exc,
            )

            return {}

    def _safe_fast_info(
        self,
        ticker: yf.Ticker,
    ) -> dict[str, Any]:

        try:

            return dict(ticker.fast_info)

        except Exception:

            return {}


    # =====================================================
    # History
    # =====================================================

    def get_history(
        self,
        symbol: str,
        start_date: date | None = None,
        end_date: date | None = None,
        period: str | None = None,
        interval: str = "1d",
        auto_adjust: bool = False,
    ) -> pd.DataFrame:
        """
        Download OHLCV history.
        """

        ticker = self._ticker(symbol)

        try:

            if period:

                df = self._retry(
                    ticker.history,
                    period=period,
                    interval=interval,
                    auto_adjust=auto_adjust,
                )

            else:

                df = self._retry(
                    ticker.history,
                    start=start_date,
                    end=end_date,
                    interval=interval,
                    auto_adjust=auto_adjust,
                )

            return self.validate_history(df)

        except Exception as exc:

            logger.exception(
                "History download failed : %s",
                symbol,
            )

            raise exc

    # =====================================================
    # Company Information
    # =====================================================

    def get_company_info(
        self,
        symbol: str,
    ) -> dict[str, Any]:

        ticker = self._ticker(symbol)

        return self._safe_info(ticker)

    def get_fast_info(
        self,
        symbol: str,
    ) -> dict[str, Any]:

        ticker = self._ticker(symbol)

        return self._safe_fast_info(ticker)

    def get_listing_date(
        self,
        symbol: str,
    ) -> date | None:
        """
        Approximate listing date from first available candle.
        """

        try:

            df = self.get_history(
                symbol,
                period="max",
            )

            if df.empty:
                return None

            return df.index.min().date()

        except Exception:

            return None

    # =====================================================
    # Corporate Actions
    # =====================================================

    def get_actions(
        self,
        symbol: str,
    ) -> pd.DataFrame:

        ticker = self._ticker(symbol)

        try:

            actions = self._retry(
                lambda: ticker.actions
            )

            if actions is None:
                return pd.DataFrame()

            if actions.empty:
                return pd.DataFrame()

            actions = actions.copy()

            actions.index = pd.to_datetime(
                actions.index
            )

            actions = actions.sort_index()

            return actions

        except Exception:

            logger.exception(
                "Unable to fetch actions : %s",
                symbol,
            )

            return pd.DataFrame()

    def get_dividends(
        self,
        symbol: str,
    ) -> pd.Series:

        ticker = self._ticker(symbol)

        try:

            return self._retry(
                lambda: ticker.dividends
            )

        except Exception:

            return pd.Series(dtype=float)

    def get_splits(
        self,
        symbol: str,
    ) -> pd.Series:

        ticker = self._ticker(symbol)

        try:

            return self._retry(
                lambda: ticker.splits
            )

        except Exception:

            return pd.Series(dtype=float)


    # =====================================================
    # Fundamentals
    # =====================================================

    def get_fundamentals(
        self,
        symbol: str,
    ) -> dict[str, Any]:

        info = self.get_company_info(symbol)
        fast = self.get_fast_info(symbol)

        return {
            "market_cap": info.get("marketCap", fast.get("marketCap")),
            "enterprise_value": info.get("enterpriseValue"),
            "pe": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "pb": info.get("priceToBook"),
            "peg_ratio": info.get("pegRatio"),
            "price_to_sales": info.get("priceToSalesTrailing12Months"),
            "book_value": info.get("bookValue"),
            "eps": info.get("trailingEps"),
            "forward_eps": info.get("forwardEps"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            "profit_margin": info.get("profitMargins"),
            "operating_margin": info.get("operatingMargins"),
            "gross_margin": info.get("grossMargins"),
            "ebitda_margin": info.get("ebitdaMargins"),
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "dividend_yield": info.get("dividendYield"),
            "dividend_rate": info.get("dividendRate"),
            "payout_ratio": info.get("payoutRatio"),
            "beta": info.get("beta"),
            "current_ratio": info.get("currentRatio"),
            "quick_ratio": info.get("quickRatio"),
            "debt_to_equity": info.get("debtToEquity"),
            "free_cash_flow": info.get("freeCashflow"),
            "operating_cash_flow": info.get("operatingCashflow"),
            "shares_outstanding": info.get("sharesOutstanding"),
            "float_shares": info.get("floatShares"),
            "held_percent_insiders": info.get("heldPercentInsiders"),
            "held_percent_institutions": info.get("heldPercentInstitutions"),
            "target_price": info.get("targetMeanPrice"),
            "recommendation": info.get("recommendationKey"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "country": info.get("country"),
            "currency": info.get("currency"),
            "exchange": info.get("exchange"),
            "website": info.get("website"),
            "employees": info.get("fullTimeEmployees"),
            "business_summary": info.get("longBusinessSummary"),
        }

    # =====================================================
    # Financial Statements
    # =====================================================

    def get_financials(
        self,
        symbol: str,
    ) -> dict[str, pd.DataFrame]:

        return {
            "income_statement": self.get_income_statement(symbol),
            "balance_sheet": self.get_balance_sheet(symbol),
            "cashflow": self.get_cashflow(symbol),
        }

    def get_income_statement(
        self,
        symbol: str,
    ) -> pd.DataFrame:

        ticker = self._ticker(symbol)

        try:

            df = self._retry(
                lambda: ticker.financials
            )

            if df is None:
                return pd.DataFrame()

            return df

        except Exception:

            logger.exception(
                "Income statement failed : %s",
                symbol,
            )

            return pd.DataFrame()

    def get_balance_sheet(
        self,
        symbol: str,
    ) -> pd.DataFrame:

        ticker = self._ticker(symbol)

        try:

            df = self._retry(
                lambda: ticker.balance_sheet
            )

            if df is None:
                return pd.DataFrame()

            return df

        except Exception:

            logger.exception(
                "Balance sheet failed : %s",
                symbol,
            )

            return pd.DataFrame()

    def get_cashflow(
        self,
        symbol: str,
    ) -> pd.DataFrame:

        ticker = self._ticker(symbol)

        try:

            df = self._retry(
                lambda: ticker.cashflow
            )

            if df is None:
                return pd.DataFrame()

            return df

        except Exception:

            logger.exception(
                "Cashflow failed : %s",
                symbol,
            )

            return pd.DataFrame()

    # =====================================================
    # Earnings
    # =====================================================

    def get_earnings(
        self,
        symbol: str,
    ) -> pd.DataFrame:

        ticker = self._ticker(symbol)

        try:

            return self._retry(
                lambda: ticker.earnings
            )

        except Exception:

            return pd.DataFrame()

    def get_quarterly_results(
        self,
        symbol: str,
    ) -> pd.DataFrame:

        ticker = self._ticker(symbol)

        try:

            return self._retry(
                lambda: ticker.quarterly_financials
            )

        except Exception:

            return pd.DataFrame()

    # =====================================================
    # Shareholders
    # =====================================================

    def get_share_holders(
        self,
        symbol: str,
    ) -> dict[str, pd.DataFrame]:

        ticker = self._ticker(symbol)

        data = {}

        try:
            data["major"] = ticker.major_holders
        except Exception:
            data["major"] = pd.DataFrame()

        try:
            data["institutional"] = ticker.institutional_holders
        except Exception:
            data["institutional"] = pd.DataFrame()

        try:
            data["mutualfund"] = ticker.mutualfund_holders
        except Exception:
            data["mutualfund"] = pd.DataFrame()

        return data

    # =====================================================
    # Analyst
    # =====================================================

    def get_analyst_targets(
        self,
        symbol: str,
    ) -> dict[str, Any]:

        info = self.get_company_info(symbol)

        return {
            "target_mean": info.get("targetMeanPrice"),
            "target_high": info.get("targetHighPrice"),
            "target_low": info.get("targetLowPrice"),
            "target_median": info.get("targetMedianPrice"),
            "recommendation": info.get("recommendationKey"),
            "recommendation_mean": info.get("recommendationMean"),
            "number_of_analysts": info.get("numberOfAnalystOpinions"),
        }

    # =====================================================
    # Health Check
    # =====================================================

    def is_available(self) -> bool:

        try:

            ticker = self._ticker("RELIANCE")

            _ = self._retry(
                lambda: ticker.fast_info
            )

            return True

        except Exception:

            logger.exception(
                "Yahoo Provider unavailable."
            )

            return False

