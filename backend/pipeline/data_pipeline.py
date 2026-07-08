import logging
import time
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Any, Tuple

import pandas as pd

from backend.core.db import get_db
from backend.providers.yahoo_provider import YahooProvider
from backend.pipeline.base_pipeline import BasePipeline


class DataPipeline(BasePipeline):
    
    def __init__(self) -> None:
        super().__init__("DataPipeline")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.provider = YahooProvider()
        self._last_dates_cache_dict: Dict[str, str] = {}
        self.max_retries = 3
        
        self.stats = {
            "processed_symbols": 0,
            "failed_symbols": 0,
            "skipped_symbols": 0,
            "history_rows": 0,
            "fundamental_rows": 0,
            "financial_rows": 0,
            "company_rows": 0,
            "corporate_action_rows": 0,
            "shareholding_rows": 0,
            "analyst_rows": 0,
            "earnings_rows": 0,
            "start_time": 0.0,
            "end_time": 0.0
        }

    def _active_symbols(self, db) -> List[str]:
        self.logger.info("Fetching active symbols...")
        query = "SELECT symbol FROM stock_master WHERE status = 'ACTIVE'"
        cursor = db.execute(query)
        return [row[0] for row in cursor.fetchall()]

    def _last_dates_cache(self, db) -> None:
        self.logger.info("Initializing last dates cache...")
        query = "SELECT symbol, MAX(date) FROM historical_data GROUP BY symbol"
        cursor = db.execute(query)
        self._last_dates_cache_dict = {row[0]: row[1] for row in cursor.fetchall()}

    def _download_start(self, symbol: str) -> str:
        last_date_str = self._last_dates_cache_dict.get(symbol)
        if last_date_str:
            try:
                last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
                # Overlap by 5 days to handle weekends, holidays, and missing candles
                next_date = last_date - timedelta(days=5)
                return next_date.strftime("%Y-%m-%d")
            except ValueError:
                self.logger.warning(f"Invalid date format in cache for {symbol}: {last_date_str}")
        return "1990-01-01"

    def _download_end(self) -> str:
        return date.today().strftime("%Y-%m-%d")

    def _download_history(self, symbol: str, start: str, end: str) -> Optional[pd.DataFrame]:
        for attempt in range(1, self.max_retries + 1):
            try:
                df = self.provider.get_history(symbol=symbol, start_date=start, end_date=end)
                return df
            except Exception as e:
                self.logger.warning(f"Retry {attempt}/{self.max_retries}: History fetch failed for {symbol}: {e}")
                if attempt == self.max_retries:
                    return None
                time.sleep(2 * attempt)
        return None

    def _download_fundamentals(self, symbol: str) -> Dict[str, Any]:
        for attempt in range(1, self.max_retries + 1):
            try:
                data = self.provider.get_fundamentals(symbol)
                return data if data else {}
            except Exception as e:
                self.logger.warning(f"Retry {attempt}/{self.max_retries}: Fundamental fetch failed for {symbol}: {e}")
                if attempt == self.max_retries:
                    return {}
                time.sleep(2 * attempt)
        return {}

    def _download_financials(self, symbol: str) -> Dict[str, Any]:
        for attempt in range(1, self.max_retries + 1):
            try:
                data = self.provider.get_financials(symbol)
                return data if data else {}
            except Exception as e:
                self.logger.warning(f"Retry {attempt}/{self.max_retries}: Financials fetch failed for {symbol}: {e}")
                if attempt == self.max_retries:
                    return {}
                time.sleep(2 * attempt)
        return {}

    def _download_company_profile(self, symbol: str) -> Dict[str, Any]:
        for attempt in range(1, self.max_retries + 1):
            try:
                data = self.provider.get_company_info(symbol)
                return data if data else {}
            except Exception as e:
                self.logger.warning(f"Retry {attempt}/{self.max_retries}: Company Profile fetch failed for {symbol}: {e}")
                if attempt == self.max_retries:
                    return {}
                time.sleep(2 * attempt)
        return {}

    def _download_actions(self, symbol: str) -> List[Dict[str, Any]]:
        for attempt in range(1, self.max_retries + 1):
            try:
                raw_df = self.provider.get_actions(symbol)
                if raw_df is not None and not raw_df.empty:
                    return self.provider.normalize_actions(raw_df)
                return []
            except Exception as e:
                self.logger.warning(f"Retry {attempt}/{self.max_retries}: Actions fetch failed for {symbol}: {e}")
                if attempt == self.max_retries:
                    return []
                time.sleep(2 * attempt)
        return []

    def _download_shareholders(self, symbol: str) -> List[Dict[str, Any]]:
        for attempt in range(1, self.max_retries + 1):
            try:
                raw_dict = self.provider.get_share_holders(symbol)
                if raw_dict:
                    return self.provider.normalize_shareholders(raw_dict)
                return []
            except Exception as e:
                self.logger.warning(f"Retry {attempt}/{self.max_retries}: Shareholders fetch failed for {symbol}: {e}")
                if attempt == self.max_retries:
                    return []
                time.sleep(2 * attempt)
        return []

    def _download_recommendation(self, symbol: str) -> Dict[str, Any]:
        for attempt in range(1, self.max_retries + 1):
            try:
                data = self.provider.get_analyst_targets(symbol)
                return data if data else {}
            except Exception as e:
                self.logger.warning(f"Retry {attempt}/{self.max_retries}: Analyst fetch failed for {symbol}: {e}")
                if attempt == self.max_retries:
                    return {}
                time.sleep(2 * attempt)
        return {}

    def _download_earnings(self, symbol: str) -> List[Dict[str, Any]]:
        for attempt in range(1, self.max_retries + 1):
            try:
                raw_df = self.provider.get_earnings_history(symbol)
                if raw_df is not None and not raw_df.empty:
                    return self.provider.normalize_earnings(raw_df)
                return []
            except Exception as e:
                self.logger.warning(f"Retry {attempt}/{self.max_retries}: Earnings fetch failed for {symbol}: {e}")
                if attempt == self.max_retries:
                    return []
                time.sleep(2 * attempt)
        return []

    def _prepare_history_rows(self, df: pd.DataFrame, symbol: str) -> List[Tuple]:
        if df is None or df.empty:
            return []
            
        df = df.copy()
        df.columns = [str(col).lower() for col in df.columns]
        
        if 'date' not in df.columns:
            df = df.reset_index()
            df.columns = [str(col).lower() for col in df.columns]
            
        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        if not all(req in df.columns for req in required_columns):
            return []
            
        df = df.dropna(subset=['open', 'high', 'low', 'close'])
        if df.empty:
            return []
            
        df = df.drop_duplicates(subset=['date'])
        df = df.sort_values(by='date')
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        
        rows = []
        for _, row in df.iterrows():
            rows.append((
                symbol,
                row['date'],
                float(row['open']),
                float(row['high']),
                float(row['low']),
                float(row['close']),
                int(row['volume'])
            ))
        return rows

    def _prepare_financial_rows(self, data: Dict[str, Any], symbol: str) -> List[Tuple]:
        if not data:
            return []
            
        merged: Dict[Tuple[int, int], Dict[str, Any]] = {}
        
        def _safe_float(val: Any) -> Optional[float]:
            try: return float(val) if val is not None else None
            except Exception: return None
            
        currency = data.get("currency")
        market_cap_val = _safe_float(data.get("market_cap"))
        enterprise_value_val = _safe_float(data.get("enterprise_value"))
        shares_out_val = _safe_float(data.get("shares_outstanding"))
        beta_val = _safe_float(data.get("beta"))
        div_yield_val = _safe_float(data.get("dividend_yield"))
        updated_at = data.get("updated_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        def merge_list(lst: List[Dict], is_quarter: bool):
            if not lst: return
            for item in lst:
                if not item: continue
                fy = item.get("fiscal_year")
                if fy is None: continue
                fq = item.get("fiscal_quarter") if is_quarter else 0
                key = (int(fy), int(fq) if fq is not None else 0)
                if key not in merged:
                    merged[key] = {}
                merged[key].update(item)

        merge_list(data.get("income_statement_annual", []), False)
        merge_list(data.get("balance_sheet_annual", []), False)
        merge_list(data.get("cashflow_annual", []), False)
        merge_list(data.get("income_statement_quarterly", []), True)
        merge_list(data.get("balance_sheet_quarterly", []), True)
        merge_list(data.get("cashflow_quarterly", []), True)

        rows = []
        for (fy, fq), metrics in merged.items():
            def sf(k: str) -> Optional[float]:
                v = metrics.get(k)
                try: return float(v) if v is not None else None
                except Exception: return None
            
            metric_market_cap = sf("market_cap")
            metric_enterprise_value = sf("enterprise_value")
            metric_shares = sf("shares_outstanding")
            metric_beta = sf("beta")
            metric_dividend_yield = sf("dividend_yield")

            mc = metric_market_cap if metric_market_cap is not None else market_cap_val
            ev = metric_enterprise_value if metric_enterprise_value is not None else enterprise_value_val
            so = metric_shares if metric_shares is not None else shares_out_val
            b = metric_beta if metric_beta is not None else beta_val
            dy = metric_dividend_yield if metric_dividend_yield is not None else div_yield_val

            rows.append((
                symbol, fy, fq, str(currency) if currency else None,
                sf("total_revenue"), sf("cost_of_revenue"), sf("gross_profit"), sf("operating_expense"),
                sf("operating_income"), sf("ebit"), sf("ebitda"), sf("pretax_income"), sf("tax_expense"),
                sf("net_income"), sf("basic_eps"), sf("diluted_eps"), sf("cash"), sf("cash_equivalents"),
                sf("short_term_investments"), sf("accounts_receivable"), sf("inventory"), sf("current_assets"),
                sf("total_assets"), sf("accounts_payable"), sf("current_liabilities"), sf("total_liabilities"),
                sf("short_term_debt"), sf("long_term_debt"), sf("total_debt"), sf("shareholder_equity"),
                sf("retained_earnings"), sf("book_value"), sf("operating_cash_flow"), sf("investing_cash_flow"),
                sf("financing_cash_flow"), sf("capital_expenditure"), sf("free_cash_flow"), sf("revenue_growth"),
                sf("earnings_growth"), sf("profit_margin"), sf("gross_margin"), sf("operating_margin"),
                sf("net_margin"), sf("roa"), sf("roe"), sf("roce"), sf("roic"),
                mc, ev, so, b,
                sf("dividend_per_share"),
                dy,
                str(metrics.get("audit_status", "")),
                updated_at
            ))
        return rows


    def _prepare_company_profile(self, data: Dict[str, Any], symbol: str) -> Optional[Tuple]:
        if not data:
            return None

        if not any(
            data.get(k)
            for k in (
                "company_name",
                "short_name",
                "long_name",
                "sector",
                "industry",
            )
        ):
            return None

        def sstr(key: str) -> Optional[str]:
            value = data.get(key)
            return str(value) if value is not None else None

        def sint(key: str) -> Optional[int]:
            value = data.get(key)
            try:
                return int(float(value)) if value is not None else None
            except Exception:
                return None

        return (
            symbol,
            sstr("company_name"),
            sstr("short_name"),
            sstr("long_name"),
            sstr("exchange"),
            sstr("exchange_code"),
            sstr("isin"),
            sstr("sector"),
            sstr("industry"),
            sstr("sub_industry"),
            sstr("market"),
            sstr("currency"),
            sstr("country"),
            sstr("state"),
            sstr("city"),
            sstr("address"),
            sstr("zipcode"),
            sstr("website"),
            sstr("phone"),
            sstr("email"),
            sstr("ceo"),
            sstr("cfo"),
            sstr("chairman"),
            sint("employees"),
            sint("founded_year"),
            sstr("business_summary"),
            sstr("logo_url"),
            sstr("timezone"),
            data.get(
                "updated_at",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

    def _prepare_action_rows(self, data: List[Dict[str, Any]], symbol: str) -> List[Tuple]:
        if not data: return []
        rows = []
        for item in data:
            if not item: continue
            date_val = item.get("action_date")
            atype = item.get("action_type")
            if not date_val or not atype: continue
            
            def sf(k):
                v = item.get(k)
                try: return float(v) if v is not None else None
                except Exception: return None
            
            rows.append((
                symbol,
                str(date_val),
                str(atype),
                sf("dividend"), sf("split_ratio"), sf("bonus_ratio"), sf("rights_ratio"),
                sf("face_value_change"), sf("buyback"), sf("merger"), sf("demerger"), sf("spin_off"),
                str(item.get("description")) if item.get("description") else None,
                item.get("updated_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            ))
        return rows

    def _prepare_shareholding_rows(self, data: List[Dict[str, Any]], symbol: str) -> List[Tuple]:
        if not data: return []
        rows = []
        for item in data:
            if not item: continue
            q = item.get("quarter")
            if not q: continue
            
            def sf(k):
                v = item.get(k)
                try: return float(v) if v is not None else None
                except Exception: return None
            
            rows.append((
                symbol,
                str(q),
                sf("promoter_holding"), sf("promoter_pledged"), sf("fii_holding"), sf("dii_holding"),
                sf("mutual_fund_holding"), sf("insurance_holding"), sf("government_holding"),
                sf("foreign_holding"), sf("retail_holding"), sf("public_holding"), sf("insider_holding"),
                sf("others_holding"), item.get("updated_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            ))
        return rows


    def _prepare_analyst_row(self, data: Dict[str, Any], symbol: str) -> Optional[Tuple]:
        if not data:
            return None

        if data.get("target_price") is None and data.get("recommendation") is None:
            return None

        def sf(key: str) -> Optional[float]:
            value = data.get(key)
            try:
                return float(value) if value is not None else None
            except Exception:
                return None

        return (
            symbol,
            sf("target_price"),
            sf("target_high"),
            sf("target_low"),
            sf("target_mean"),
            str(data.get("recommendation")) if data.get("recommendation") else None,
            str(data.get("recommendation_key")) if data.get("recommendation_key") else None,
            self.provider.safe_int(data.get("number_of_analysts")),
            data.get(
                "updated_at",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

    def _prepare_earnings_rows(self, data: List[Dict[str, Any]], symbol: str) -> List[Tuple]:
        if not data: return []
        rows = []
        for item in data:
            if not item: continue
            q = item.get("quarter")
            if not q: continue
            
            def sf(k):
                v = item.get(k)
                try: return float(v) if v is not None else None
                except Exception: return None
            
            rows.append((
                symbol,
                str(q),
                sf("estimate"), sf("reported"), sf("surprise"), sf("surprise_percent"),
                item.get("updated_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            ))
        return rows

    def _bulk_insert_history(self, db, rows: List[Tuple]) -> int:
        if not rows:
            return 0

        query = """
            INSERT OR IGNORE INTO historical_data
            (symbol, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        db.executemany(query, rows)
        return len(rows)

    def _save_fundamentals(self, db, symbol: str, fundamentals: Dict[str, Any]) -> bool:
        if not fundamentals or (fundamentals.get("market_cap") is None and fundamentals.get("pe") is None):
            return False
            
        query = """
            INSERT OR REPLACE INTO fundamental_data (
                symbol, market_cap, pe, pb, roe, roce, debt_equity,
                sales_growth, profit_growth, promoter_holding, institutional_holding,
                fii_holding, dii_holding, dividend_yield, sector, industry, eps,
                book_value, current_ratio, quick_ratio, operating_margin, net_margin,
                cash, free_cash_flow, enterprise_value, beta, week52_high, week52_low,
                target_price, recommendation, shares_outstanding, updated_at
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """
        def sf(val: Any) -> Optional[float]:
            try: return float(val) if val is not None else None
            except Exception: return None

        data_tuple = (
            symbol, sf(fundamentals.get('market_cap')), sf(fundamentals.get('pe')), sf(fundamentals.get('pb')),
            sf(fundamentals.get('roe')), sf(fundamentals.get('roce')),
            sf(fundamentals.get('debt_to_equity', fundamentals.get('debt_equity'))),
            sf(fundamentals.get('sales_growth')), sf(fundamentals.get('profit_growth')),
            sf(fundamentals.get('promoter_holding')), sf(fundamentals.get('institutional_holding')),
            sf(fundamentals.get('fii_holding')), sf(fundamentals.get('dii_holding')),
            sf(fundamentals.get('dividend_yield')),
            str(fundamentals.get('sector')) if fundamentals.get('sector') else None,
            str(fundamentals.get('industry')) if fundamentals.get('industry') else None,
            sf(fundamentals.get('eps')), sf(fundamentals.get('book_value')), sf(fundamentals.get('current_ratio')),
            sf(fundamentals.get('quick_ratio')), sf(fundamentals.get('operating_margin')), sf(fundamentals.get('net_margin')),
            sf(fundamentals.get('cash')), sf(fundamentals.get('free_cash_flow')), sf(fundamentals.get('enterprise_value')),
            sf(fundamentals.get('beta')),
            sf(fundamentals.get('week52_high', fundamentals.get('52_week_high', fundamentals.get('fiftyTwoWeekHigh')))),
            sf(fundamentals.get('week52_low', fundamentals.get('52_week_low', fundamentals.get('fiftyTwoWeekLow')))),
            sf(fundamentals.get('target_price')),
            str(fundamentals.get('recommendation')) if fundamentals.get('recommendation') else None,
            sf(fundamentals.get('shares_outstanding')),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.execute(query, data_tuple)
        return True

    def _save_financials(self, db, rows: List[Tuple]) -> int:
        if not rows: return 0
        query = """
            INSERT OR REPLACE INTO financial_data (
                symbol, fiscal_year, fiscal_quarter, currency, total_revenue, cost_of_revenue, gross_profit,
                operating_expense, operating_income, ebit, ebitda, pretax_income, tax_expense, net_income,
                basic_eps, diluted_eps, cash, cash_equivalents, short_term_investments, accounts_receivable,
                inventory, current_assets, total_assets, accounts_payable, current_liabilities, total_liabilities,
                short_term_debt, long_term_debt, total_debt, shareholder_equity, retained_earnings, book_value,
                operating_cash_flow, investing_cash_flow, financing_cash_flow, capital_expenditure, free_cash_flow,
                revenue_growth, earnings_growth, profit_margin, gross_margin, operating_margin, net_margin,
                roa, roe, roce, roic, market_cap, enterprise_value, shares_outstanding, beta, dividend_per_share,
                dividend_yield, audit_status, updated_at
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """
        db.executemany(query, rows)
        return len(rows)

    def _save_company_profile(self, db, row: Tuple) -> bool:
        if not row: return False
        query = """
            INSERT OR REPLACE INTO company_profile (
                symbol, company_name, short_name, long_name, exchange, exchange_code, isin, sector, industry,
                sub_industry, market, currency, country, state, city, address, zipcode, website, phone, email,
                ceo, cfo, chairman, employees, founded_year, business_summary, logo_url, timezone, updated_at
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """
        db.execute(query, row)
        return True

    def _save_actions(self, db, rows: List[Tuple]) -> int:
        if not rows: return 0
        query = """
            INSERT OR IGNORE INTO corporate_actions (
                symbol, action_date, action_type, dividend, split_ratio, bonus_ratio, rights_ratio,
                face_value_change, buyback, merger, demerger, spin_off, description, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        db.executemany(query, rows)
        return len(rows)

    def _save_shareholders(self, db, rows: List[Tuple]) -> int:
        if not rows: return 0
        query = """
            INSERT OR REPLACE INTO shareholding_data (
                symbol, quarter, promoter_holding, promoter_pledged, fii_holding, dii_holding,
                mutual_fund_holding, insurance_holding, government_holding, foreign_holding,
                retail_holding, public_holding, insider_holding, others_holding, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        db.executemany(query, rows)
        return len(rows)

    def _save_analyst(self, db, row: Tuple) -> bool:
        if not row: return False
        query = """
            INSERT OR REPLACE INTO analyst_data (
                symbol, target_price, target_high, target_low, target_mean,
                recommendation, recommendation_key, number_of_analysts, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        db.execute(query, row)
        return True

    def _save_earnings(self, db, rows: List[Tuple]) -> int:
        if not rows: return 0
        query = """
            INSERT OR REPLACE INTO earnings_history (
                symbol, quarter, estimate, reported, surprise, surprise_percent, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        db.executemany(query, rows)
        return len(rows)

    def _update_log(self, db, status: str) -> None:
        if status == "RUNNING":
            status_string = "RUNNING"
        else:
            exec_time = max(0.0, self.stats["end_time"] - self.stats["start_time"])
            status_string = f"{status} | Processed: {self.stats['processed_symbols']} | Failed: {self.stats['failed_symbols']} | Skipped: {self.stats['skipped_symbols']} | Time: {exec_time:.2f}s"
        
        query = """
            INSERT OR REPLACE INTO update_log (process_name, last_run, status)
            VALUES (?, ?, ?)
        """
        db.execute(
            query,
            (
                "DATA_PIPELINE",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status_string,
            ),
        )

    def _history_statistics(self, total_symbols: int) -> None:
        exec_time = max(0.0, self.stats["end_time"] - self.stats["start_time"])
        
        self.logger.info("="*50)
        self.logger.info("PIPELINE STATISTICS")
        self.logger.info("="*50)
        self.logger.info(f"Total Symbols          : {total_symbols}")
        self.logger.info(f"Processed Symbols      : {self.stats['processed_symbols']}")
        self.logger.info(f"Failed Symbols         : {self.stats['failed_symbols']}")
        self.logger.info(f"Skipped Symbols        : {self.stats['skipped_symbols']}")
        self.logger.info("-" * 50)
        self.logger.info(f"History Rows           : {self.stats['history_rows']}")
        self.logger.info(f"Fundamental Rows       : {self.stats['fundamental_rows']}")
        self.logger.info(f"Financial Rows         : {self.stats['financial_rows']}")
        self.logger.info(f"Company Rows           : {self.stats['company_rows']}")
        self.logger.info(f"Corporate Action Rows  : {self.stats['corporate_action_rows']}")
        self.logger.info(f"Shareholding Rows      : {self.stats['shareholding_rows']}")
        self.logger.info(f"Analyst Rows           : {self.stats['analyst_rows']}")
        self.logger.info(f"Earnings Rows          : {self.stats['earnings_rows']}")
        self.logger.info("-" * 50)
        self.logger.info(f"Execution Time         : {exec_time:.2f}s")
        self.logger.info("="*50)

    def run(self) -> None:
        self.logger.info("Pipeline Start")
        self.stats["start_time"] = time.time()
        
        if not self.provider.is_available():
            self.logger.error("Provider is unavailable. Aborting pipeline.")
            self.stats["end_time"] = time.time()
            return

        try:
            with get_db() as db:
                db.execute("PRAGMA journal_mode=WAL;")
                db.execute("PRAGMA synchronous=NORMAL;")
                db.execute("PRAGMA temp_store=MEMORY;")
                db.execute("PRAGMA foreign_keys=ON;")
                
                self._update_log(db, "RUNNING")
                
                self._last_dates_cache(db)
                symbols = self._active_symbols(db)
                total_symbols = len(symbols)
                
                end_date = self._download_end()
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                
                for index, symbol in enumerate(symbols, 1):
                    self.logger.info(f"Current Symbol: {symbol} ({index}/{total_symbols})")
                    has_fatal_error = False

                    success_count = 0
                    empty_count = 0
                    failed_count = 0
                    failed_modules = []

                    symbol_start = time.perf_counter()
                    
                    try:

                        start_date = self._download_start(symbol)
                        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                        
                        if start_dt > end_dt:
                            self.stats["skipped_symbols"] += 1
                            continue
                            
                                                # History Module
                        try:
                            df_history = self._download_history(symbol, start_date, end_date)
                            rows = self._prepare_history_rows(df_history, symbol)
                            if rows:
                                inserted_count = self._bulk_insert_history(db, rows)
                                if rows:
                                    success_count += 1
                                else:
                                    empty_count += 1
                                self.stats["history_rows"] += inserted_count
                                success_count += 1
                                max_date = max(row[1] for row in rows)
                                self._last_dates_cache_dict[symbol] = max_date
                        except Exception as e:
                            failed_count += 1
                            failed_modules.append("History")
                            self.logger.error(f"History failure for {symbol}: {e}")
                            
                                                # Fundamentals Module
                        try:
                            fundamentals = self._download_fundamentals(symbol)
                            if self._save_fundamentals(db, symbol, fundamentals):
                                self.stats["fundamental_rows"] += 1
                                success_count += 1
                            else:
                                empty_count += 1
                                self.stats["fundamental_rows"] += 1
                                success_count += 1
                        except Exception as e:
                            failed_count += 1
                            failed_modules.append("Fundamentals")
                            self.logger.error(f"Fundamentals failure for {symbol}: {e}")
                            
                                                # Financials Module
                        try:
                            financial_data = self._download_financials(symbol)
                            fin_rows = self._prepare_financial_rows(financial_data, symbol)
                            if fin_rows:
                                success_count += 1
                                inserted_count = self._save_financials(db, fin_rows)
                                self.stats["financial_rows"] += inserted_count
                                success_count += 1
                        except Exception as e:
                            failed_count += 1
                            failed_modules.append("Financials")
                            self.logger.error(f"Financials failure for {symbol}: {e}")
                            
                                                # Company Profile Module
                        try:
                            profile_data = self._download_company_profile(symbol)
                            prof_row = self._prepare_company_profile(profile_data, symbol)
                            if prof_row:
                                if self._save_company_profile(db, prof_row):
                                    self.stats["company_rows"] += 1
                                    success_count += 1
                            else:
                                empty_count += 1
                                if self._save_company_profile(db, prof_row):
                                    self.stats["company_rows"] += 1
                                    success_count += 1
                        except Exception as e:
                            failed_count += 1
                            failed_modules.append("Company")
                            self.logger.error(f"Company Profile failure for {symbol}: {e}")
                            
                                                # Corporate Actions Module (disabled)
                        empty_count += 1
                            
                                                # Shareholding Module
                        try:
                            share_data = self._download_shareholders(symbol)
                            share_rows = self._prepare_shareholding_rows(share_data, symbol)
                            if share_rows:
                                success_count += 1
                                inserted_count = self._save_shareholders(db, share_rows)
                                self.stats["shareholding_rows"] += inserted_count
                                success_count += 1
                        except Exception as e:
                            failed_count += 1
                            failed_modules.append("Shareholding")
                            self.logger.error(f"Shareholders failure for {symbol}: {e}")
                            
                                                # Analyst Module
                        try:
                            analyst_data = self._download_recommendation(symbol)
                            analyst_row = self._prepare_analyst_row(analyst_data, symbol)
                            if analyst_row:
                                success_count += 1
                                if self._save_analyst(db, analyst_row):
                                    self.stats["analyst_rows"] += 1
                                    success_count += 1
                        except Exception as e:
                            failed_count += 1
                            failed_modules.append("Analyst")
                            self.logger.error(f"Analyst Recommendations failure for {symbol}: {e}")
                            
                                                # Earnings Module
                        try:
                            earnings_data = self._download_earnings(symbol)
                            earnings_rows = self._prepare_earnings_rows(earnings_data, symbol)
                            if earnings_rows:
                                success_count += 1
                                inserted_count = self._save_earnings(db, earnings_rows)
                                self.stats["earnings_rows"] += inserted_count
                                success_count += 1
                        except Exception as e:
                            failed_count += 1
                            failed_modules.append("Earnings")
                            self.logger.error(f"Earnings failure for {symbol}: {e}")
                            
                        self.stats["processed_symbols"] += 1
                        
                    except Exception as e:
                        has_fatal_error = True
                        self.logger.error(f"Failures processing {symbol}: {e}")
                        
                        
                    elapsed = time.perf_counter() - symbol_start

                    eta = ((time.time() - self.stats["start_time"]) / index) * (total_symbols - index)

                    eta_min = int(eta // 60)
                    eta_sec = int(eta % 60)

                    print(
                        f"[{index:04d}/{total_symbols}] "
                        f"{symbol:<15} "
                        f"✓{success_count} "
                        f"○{empty_count} "
                        f"✗{failed_count} "
                        f"{elapsed:.2f}s",
                        flush=True,
                    )

                    if has_fatal_error:
                        self.stats["failed_symbols"] += 1

                self.stats["end_time"] = time.time()
                self._history_statistics(total_symbols)
                self._update_log(db, "COMPLETED")
                self.logger.info("Pipeline Finished")
                
        except Exception as e:
            self.stats["end_time"] = time.time()
            self.logger.error(f"Fatal Pipeline Error: {e}")
            try:
                with get_db() as emergency_db:
                    self._update_log(emergency_db, "FAILED")
            except Exception:
                pass


if __name__ == "__main__":
    DataPipeline().execute()
