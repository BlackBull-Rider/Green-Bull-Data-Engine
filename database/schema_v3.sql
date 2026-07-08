CREATE TABLE IF NOT EXISTS financial_data (

    symbol TEXT PRIMARY KEY,

    total_revenue REAL,
    gross_profit REAL,
    operating_income REAL,
    net_income REAL,

    total_assets REAL,
    total_liabilities REAL,

    shareholder_equity REAL,

    operating_cash_flow REAL,
    free_cash_flow REAL,

    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS company_profile (

    symbol TEXT PRIMARY KEY,

    company_name TEXT,

    sector TEXT,

    industry TEXT,

    website TEXT,

    country TEXT,

    city TEXT,

    employees INTEGER,

    business_summary TEXT,

    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS corporate_actions (

    symbol TEXT NOT NULL,

    action_date TEXT NOT NULL,

    action_type TEXT NOT NULL,

    value REAL,

    PRIMARY KEY
    (
        symbol,
        action_date,
        action_type
    )
);

CREATE TABLE IF NOT EXISTS shareholding_data (

    symbol TEXT PRIMARY KEY,

    insider REAL,

    institutional REAL,

    mutual_fund REAL,

    foreign REAL,

    public REAL,

    updated_at TEXT
);
