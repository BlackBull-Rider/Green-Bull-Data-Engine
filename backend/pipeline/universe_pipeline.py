"""
NEW AI BULL V1

Universe Pipeline

Python 3.13
"""

from __future__ import annotations

import logging

from backend.core.db import get_db
from backend.pipeline.base_pipeline import BasePipeline
from backend.providers.nse_provider import NSEProvider

logger = logging.getLogger(__name__)


class UniversePipeline(BasePipeline):

    def __init__(self):

        super().__init__("Universe")

        self.provider = NSEProvider()

    # =====================================================
    # Database
    # =====================================================

    def _load_existing(self) -> dict:

        with get_db() as conn:

            rows = conn.execute(
                """
                SELECT
                    symbol,
                    company_name,
                    exchange,
                    status
                FROM stock_master
                """
            ).fetchall()

        return {
            row["symbol"]: row
            for row in rows
        }

    def _mark_all_delisted(self):

        with get_db() as conn:

            conn.execute(
                """
                UPDATE stock_master

                SET

                    status='DELISTED',
                    updated_at=datetime('now')
                """
            )

    def _insert_symbol(
        self,
        conn,
        symbol,
        company,
        exchange,
    ):

        conn.execute(
            """
            INSERT INTO stock_master
            (
                symbol,
                company_name,
                exchange,
                status,
                updated_at
            )

            VALUES
            (
                ?,
                ?,
                ?,
                'ACTIVE',
                datetime('now')
            )
            """,
            (
                symbol,
                company,
                exchange,
            ),
        )

    def _update_symbol(
        self,
        conn,
        symbol,
        company,
        exchange,
    ):

        conn.execute(
            """
            UPDATE stock_master

            SET

                company_name=?,
                exchange=?,
                status='ACTIVE',
                updated_at=datetime('now')

            WHERE symbol=?
            """,
            (
                company,
                exchange,
                symbol,
            ),
        )

    # =====================================================
    # Main
    # =====================================================

    def run(self):

        self.log(
            "Downloading NSE Universe..."
        )

        universe = self.provider.get_universe()

        if universe.empty:

            raise RuntimeError(
                "Universe Empty"
            )

        universe.columns = [
            c.lower().strip()
            for c in universe.columns
        ]

        universe = universe.drop_duplicates(
            subset="symbol"
        )

        universe = universe.sort_values(
            "symbol"
        )

        self._mark_all_delisted()

        existing = self._load_existing()

        inserted = 0

        updated = 0

        with get_db() as conn:

            for row in universe.itertuples(index=False):

                symbol = str(row.symbol).strip().upper()

                company = str(
                    row.company_name
                ).strip()

                exchange = str(
                    row.exchange
                ).strip()

                if symbol not in existing:

                    self._insert_symbol(
                        conn,
                        symbol,
                        company,
                        exchange,
                    )

                    inserted += 1

                else:

                    db = existing[symbol]

                    if (
                        db["company_name"] != company
                        or
                        db["exchange"] != exchange
                        or
                        db["status"] != "ACTIVE"
                    ):

                        self._update_symbol(
                            conn,
                            symbol,
                            company,
                            exchange,
                        )

                        updated += 1

        with get_db() as conn:

            active = conn.execute(
                """
                SELECT COUNT(*)
                FROM stock_master
                WHERE status='ACTIVE'
                """
            ).fetchone()[0]

            delisted = conn.execute(
                """
                SELECT COUNT(*)
                FROM stock_master
                WHERE status='DELISTED'
                """
            ).fetchone()[0]

        self.log(
            f"Universe Size : {len(universe)}"
        )

        self.log(
            f"Inserted : {inserted}"
        )

        self.log(
            f"Updated : {updated}"
        )

        self.log(
            f"Active : {active}"
        )

        self.log(
            f"Delisted : {delisted}"
        )

        self.log(
            "Universe Pipeline Completed."
        )


if __name__ == "__main__":

    UniversePipeline().execute()

