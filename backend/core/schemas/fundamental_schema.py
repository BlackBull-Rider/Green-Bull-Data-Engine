"""
GREEN BULL DATA ENGINE
Fundamental Schema
"""

from __future__ import annotations

import logging
import sqlite3

logger = logging.getLogger(__name__)


def create_fundamental_tables(conn: sqlite3.Connection) -> None:
    """
    Creates all fundamental & financial tables.
    Safe to run multiple times.
    """

    cursor = conn.cursor()

    # ==========================================================
    # FUNDAMENTAL DATA
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fundamental_data (

        symbol TEXT PRIMARY KEY,

        market_cap REAL,

        pe REAL,
        pb REAL,

        roe REAL,
        roce REAL,

        debt_equity REAL,

        sales_growth REAL,
        profit_growth REAL,

        promoter_holding REAL,
        institutional_holding REAL,
        fii_holding REAL,
        dii_holding REAL,

        dividend_yield REAL,

        sector TEXT,
        industry TEXT,

        eps REAL,
        book_value REAL,

        current_ratio REAL,
        quick_ratio REAL,

        operating_margin REAL,
        net_margin REAL,

        cash REAL,
        free_cash_flow REAL,

        enterprise_value REAL,

        beta REAL,

        week52_high REAL,
        week52_low REAL,

        target_price REAL,

        recommendation TEXT,

        shares_outstanding REAL,

        updated_at TEXT

    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_fundamental_sector
    ON fundamental_data(sector);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_fundamental_industry
    ON fundamental_data(industry);
    """)

    # ==========================================================
    # FINANCIAL DATA
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_data (

        symbol TEXT NOT NULL,

        fiscal_year INTEGER NOT NULL,
        fiscal_quarter TEXT NOT NULL,

        currency TEXT,

        total_revenue REAL,
        cost_of_revenue REAL,
        gross_profit REAL,
        operating_expense REAL,
        operating_income REAL,
        ebit REAL,
        ebitda REAL,
        pretax_income REAL,
        tax_expense REAL,
        net_income REAL,

        basic_eps REAL,
        diluted_eps REAL,

        cash REAL,
        cash_equivalents REAL,
        short_term_investments REAL,
        accounts_receivable REAL,
        inventory REAL,
        current_assets REAL,
        total_assets REAL,

        accounts_payable REAL,
        current_liabilities REAL,
        total_liabilities REAL,

        short_term_debt REAL,
        long_term_debt REAL,
        total_debt REAL,

        shareholder_equity REAL,
        retained_earnings REAL,
        book_value REAL,

        operating_cash_flow REAL,
        investing_cash_flow REAL,
        financing_cash_flow REAL,
        capital_expenditure REAL,
        free_cash_flow REAL,

        revenue_growth REAL,
        earnings_growth REAL,

        profit_margin REAL,
        gross_margin REAL,
        operating_margin REAL,
        net_margin REAL,

        roa REAL,
        roe REAL,
        roce REAL,
        roic REAL,

        market_cap REAL,
        enterprise_value REAL,
        shares_outstanding REAL,

        beta REAL,

        dividend_per_share REAL,
        dividend_yield REAL,

        audit_status TEXT,

        updated_at TEXT,

        PRIMARY KEY (
            symbol,
            fiscal_year,
            fiscal_quarter
        )

    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_financial_symbol
    ON financial_data(symbol);
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_financial_year
    ON financial_data(fiscal_year);
    """)

    # ==========================================================
    # SHAREHOLDING DATA
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shareholding_data (

        symbol TEXT NOT NULL,

        quarter TEXT NOT NULL,

        promoter_holding REAL,
        promoter_pledged REAL,

        fii_holding REAL,
        dii_holding REAL,

        mutual_fund_holding REAL,
        insurance_holding REAL,
        government_holding REAL,

        foreign_holding REAL,

        retail_holding REAL,
        public_holding REAL,

        insider_holding REAL,
        others_holding REAL,

        updated_at TEXT,

        PRIMARY KEY (
            symbol,
            quarter
        )

    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_shareholding_symbol
    ON shareholding_data(symbol);
    """)

    # ==========================================================
    # ANALYST DATA
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyst_data (

        symbol TEXT PRIMARY KEY,

        target_price REAL,
        target_high REAL,
        target_low REAL,
        target_mean REAL,

        recommendation TEXT,
        recommendation_key TEXT,

        number_of_analysts INTEGER,

        updated_at TEXT

    );
    """)

    # ==========================================================
    # EARNINGS HISTORY
    # ==========================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS earnings_history (

        symbol TEXT NOT NULL,

        quarter TEXT NOT NULL,

        estimate REAL,
        reported REAL,

        surprise REAL,
        surprise_percent REAL,

        updated_at TEXT,

        PRIMARY KEY (
            symbol,
            quarter
        )

    );
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_earnings_symbol
    ON earnings_history(symbol);
    """)

    conn.commit()

    logger.info("Fundamental schema initialized successfully.")
