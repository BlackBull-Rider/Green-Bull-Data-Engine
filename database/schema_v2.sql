PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;

-- =========================================================
-- Green Bull Rider V2
-- Core Schema
-- =========================================================

-- =========================================================
-- Stock Master
-- =========================================================

CREATE TABLE IF NOT EXISTS stock_master (

    symbol TEXT PRIMARY KEY,

    company_name TEXT NOT NULL,

    exchange TEXT,

    isin TEXT,

    sector TEXT,

    industry TEXT,

    listing_date TEXT,

    active INTEGER DEFAULT 1,

    created_at TEXT,

    updated_at TEXT

);

CREATE INDEX idx_stock_sector
ON stock_master(sector);

CREATE INDEX idx_stock_industry
ON stock_master(industry);

-- =========================================================
-- Market Data
-- =========================================================

CREATE TABLE IF NOT EXISTS market_data (

    symbol TEXT NOT NULL,

    date TEXT NOT NULL,

    open REAL NOT NULL,

    high REAL NOT NULL,

    low REAL NOT NULL,

    close REAL NOT NULL,

    volume REAL,

    delivery_qty REAL,

    delivery_percent REAL,

    trade_count INTEGER,

    vwap REAL,

    PRIMARY KEY(symbol,date),

    FOREIGN KEY(symbol)
        REFERENCES stock_master(symbol)

);

CREATE INDEX idx_market_symbol
ON market_data(symbol);

CREATE INDEX idx_market_date
ON market_data(date);

CREATE INDEX idx_market_symbol_date
ON market_data(symbol,date);

-- =========================================================
-- Technical Indicator Cache
-- =========================================================

CREATE TABLE IF NOT EXISTS technical_indicators (

    symbol TEXT NOT NULL,

    date TEXT NOT NULL,

    ema20 REAL,
    ema50 REAL,
    ema200 REAL,

    sma20 REAL,
    sma50 REAL,
    sma200 REAL,

    hma20 REAL,

    vwma20 REAL,

    kama20 REAL,

    rsi14 REAL,

    macd REAL,

    macd_signal REAL,

    macd_hist REAL,

    atr14 REAL,

    adx14 REAL,

    plus_di REAL,

    minus_di REAL,

    supertrend REAL,

    trend TEXT,

    bb_upper REAL,

    bb_middle REAL,

    bb_lower REAL,

    kc_upper REAL,

    kc_middle REAL,

    kc_lower REAL,

    obv REAL,

    cmf REAL,

    mfi REAL,

    vwap REAL,

    regression REAL,

    regression_slope REAL,

    regression_angle REAL,

    volatility_score REAL,

    liquidity_score REAL,

    PRIMARY KEY(symbol,date),

    FOREIGN KEY(symbol)
        REFERENCES stock_master(symbol)

);

CREATE INDEX idx_indicator_symbol
ON technical_indicators(symbol);

CREATE INDEX idx_indicator_date
ON technical_indicators(date);

CREATE INDEX idx_indicator_symbol_date
ON technical_indicators(symbol,date);

-- =========================================================
-- Fundamental Metrics
-- =========================================================

CREATE TABLE IF NOT EXISTS fundamental_metrics (

    symbol TEXT PRIMARY KEY,

    market_cap REAL,

    enterprise_value REAL,

    pe REAL,

    pb REAL,

    peg REAL,

    ev_ebitda REAL,

    eps REAL,

    book_value REAL,

    dividend_yield REAL,

    roe REAL,

    roce REAL,

    roa REAL,

    debt_equity REAL,

    current_ratio REAL,

    quick_ratio REAL,

    operating_margin REAL,

    net_margin REAL,

    gross_margin REAL,

    sales_growth REAL,

    profit_growth REAL,

    eps_growth REAL,

    free_cash_flow REAL,

    cash REAL,

    shares_outstanding REAL,

    beta REAL,

    week52_high REAL,

    week52_low REAL,

    target_price REAL,

    recommendation TEXT,

    sector TEXT,

    industry TEXT,

    updated_at TEXT,

    FOREIGN KEY(symbol)
        REFERENCES stock_master(symbol)

);

CREATE INDEX idx_fundamental_sector
ON fundamental_metrics(sector);

CREATE INDEX idx_fundamental_symbol
ON fundamental_metrics(symbol);

-- =========================================================
-- Institutional Metrics
-- =========================================================

CREATE TABLE IF NOT EXISTS institutional_metrics (

    symbol TEXT PRIMARY KEY,

    promoter_holding REAL,

    promoter_change REAL,

    institutional_holding REAL,

    fii_holding REAL,

    fii_change REAL,

    dii_holding REAL,

    dii_change REAL,

    mutual_fund_holding REAL,

    mutual_fund_change REAL,

    delivery_percent REAL,

    delivery_quantity REAL,

    bulk_deals INTEGER,

    block_deals INTEGER,

    pledged_percent REAL,

    last_updated TEXT,

    FOREIGN KEY(symbol)
        REFERENCES stock_master(symbol)

);

CREATE INDEX idx_inst_symbol
ON institutional_metrics(symbol);

-- =========================================================
-- IPO Metrics
-- =========================================================

CREATE TABLE IF NOT EXISTS ipo_metrics (

    symbol TEXT PRIMARY KEY,

    listing_date TEXT,

    listing_price REAL,

    current_price REAL,

    issue_size REAL,

    lot_size INTEGER,

    gmp REAL,

    subscription_qib REAL,

    subscription_hni REAL,

    subscription_retail REAL,

    subscription_total REAL,

    promoter_holding REAL,

    institutional_holding REAL,

    market_cap REAL,

    volume_ratio REAL,

    below_listing INTEGER,

    lockin_end_date TEXT,

    updated_at TEXT,

    FOREIGN KEY(symbol)
        REFERENCES stock_master(symbol)

);

CREATE INDEX idx_ipo_listing
ON ipo_metrics(listing_date);

-- =========================================================
-- Market Regime
-- =========================================================

CREATE TABLE IF NOT EXISTS market_regime (

    trade_date TEXT PRIMARY KEY,

    regime TEXT,

    volatility_regime TEXT,

    breadth REAL,

    advance_decline REAL,

    bullish_percent REAL,

    bearish_percent REAL,

    sector_leader TEXT,

    sector_laggard TEXT,

    risk_mode TEXT,

    market_strength REAL,

    trend_score REAL,

    updated_at TEXT

);

CREATE INDEX idx_regime_date
ON market_regime(trade_date);
