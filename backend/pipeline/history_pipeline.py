"""
NEW AI BULL V1

History Pipeline

Responsibilities
----------------
1. Full History Download
2. Incremental Update
3. Missing Candle Repair

Python 3.13
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta

import pandas as pd

from backend.core.db import get_db
from backend.pipeline.base_pipeline import BasePipeline
from backend.providers.yahoo_provider import YahooProvider

logger = logging.getLogger(__name__)


class HistoryPipeline(BasePipeline):

    def __init__(self):

        super().__init__("History")

        self.provider = YahooProvider()

    # =====================================================
    # Database Helpers
    # =====================================================

    def _active_symbols(self) -> list[str]:

        with get_db() as conn:

            rows = conn.execute(
                """
                SELECT symbol

                FROM stock_master

                WHERE status='ACTIVE'

                ORDER BY symbol
                """
            ).fetchall()

        return [
            row["symbol"]
            for row in rows
        ]

    def _last_date(
        self,
        symbol: str,
    ) -> date | None:

        with get_db() as conn:

            row = conn.execute(
                """
                SELECT
                    MAX(date)

                FROM historical_data

                WHERE symbol=?
                """,
                (
                    symbol,
                ),
            ).fetchone()

        if row is None:
            return None

        value = row[0]

        if value is None:
            return None

        return datetime.strptime(
            value,
            "%Y-%m-%d",
        ).date()

    def _history_exists(
        self,
        symbol: str,
    ) -> bool:

        return self._last_date(symbol) is not None

    def _download_start(
        self,
        symbol: str,
    ) -> date:

        last = self._last_date(symbol)

        if last is None:
            return date(1990, 1, 1)

        return last + timedelta(days=1)

    def _download_end(self) -> date:

        return date.today()


        return date.today()

    # =====================================================
    # Statistics
    # =====================================================

    def _count_rows(
        self,
        symbol: str,
    ) -> int:

        with get_db() as conn:

            row = conn.execute(
                """
                SELECT COUNT(*)

                FROM historical_data

                WHERE symbol=?
                """,
                (
                    symbol,
                ),
            ).fetchone()

        return row[0]


    # =====================================================
    # Download
    # =====================================================

    def _download_history(
        self,
        symbol: str,
    ) -> pd.DataFrame:

        start = self._download_start(symbol)

        end = self._download_end()

        if start > end:

            return pd.DataFrame()

        self.log(
            f"{symbol} : {start} -> {end}"
        )

        try:

            df = self.provider.get_history(
                symbol=symbol,
                start_date=start,
                end_date=end + timedelta(days=1),
            )

        except Exception as exc:

            logger.exception(
                "Download failed : %s",
                symbol,
            )

            raise exc

        if df is None:

            return pd.DataFrame()

        if df.empty:

            return pd.DataFrame()

        df = df.copy()

        df.index = pd.to_datetime(
            df.index
        )

        df = df.sort_index()

        df = df[
            ~df.index.duplicated()
        ]

        df = df.reset_index()

        if "Date" in df.columns:

            df.rename(
                columns={
                    "Date": "date",
                },
                inplace=True,
            )

        elif "index" in df.columns:

            df.rename(
                columns={
                    "index": "date",
                },
                inplace=True,
            )

        df["date"] = pd.to_datetime(
            df["date"]
        ).dt.strftime(
            "%Y-%m-%d"
        )

        required = [
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]

        for col in required:

            if col not in df.columns:

                raise RuntimeError(
                    f"{symbol} Missing Column : {col}"
                )

        df = df[
            required
        ]

        df.insert(
            0,
            "symbol",
            symbol,
        )

        df = df.dropna(
            subset=[
                "open",
                "high",
                "low",
                "close",
            ]
        )

        return df

    # =====================================================
    # Prepare Rows
    # =====================================================

    def _rows(
        self,
        df: pd.DataFrame,
    ) -> list[tuple]:

        if df.empty:

            return []

        rows = []

        for row in df.itertuples(index=False):

            rows.append(
                (
                    row.symbol,
                    row.date,
                    float(row.open),
                    float(row.high),
                    float(row.low),
                    float(row.close),
                    float(row.volume),
                )
            )

        return rows


    # =====================================================
    # Database Write
    # =====================================================

    def _bulk_insert(
        self,
        rows: list[tuple],
    ) -> int:

        if not rows:
            return 0

        with get_db() as conn:

            conn.executemany(
                """
                INSERT OR IGNORE INTO historical_data
                (
                    symbol,
                    date,
                    open,
                    high,
                    low,
                    close,
                    volume
                )

                VALUES
                (
                    ?,?,?,?,?,?,?
                )
                """,
                rows,
            )

        return len(rows)

    # =====================================================
    # Pipeline
    # =====================================================

    def run(self):

        symbols = self._active_symbols()

        total_symbols = len(symbols)

        inserted_rows = 0

        skipped = 0

        failed = 0

        self.log(
            f"Active Symbols : {total_symbols}"
        )

        for index, symbol in enumerate(symbols, start=1):

            self.log(
                f"[{index}/{total_symbols}] {symbol}"
            )

            try:

                df = self._download_history(
                    symbol
                )

                if df.empty:

                    skipped += 1

                    continue

                rows = self._rows(df)

                inserted_rows += self._bulk_insert(
                    rows
                )

            except Exception:

                failed += 1

                logger.exception(
                    "History Sync Failed : %s",
                    symbol,
                )

                continue

        self.log("")

        self.log(
            "History Pipeline Finished"
        )

        self.log(
            f"Processed : {total_symbols}"
        )

        self.log(
            f"Inserted Rows : {inserted_rows}"
        )

        self.log(
            f"Skipped : {skipped}"
        )

        self.log(
            f"Failed : {failed}"
        )


if __name__ == "__main__":

    HistoryPipeline().execute()

