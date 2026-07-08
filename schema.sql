CREATE TABLE historical_data(

        symbol TEXT NOT NULL,

        date TEXT NOT NULL,

        open REAL,
        high REAL,
        low REAL,
        close REAL,

        volume REAL,

        PRIMARY KEY(symbol,date)

    );
CREATE TABLE fundamental_data(

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

        updated_at TEXT
    , dividend_yield REAL, sector TEXT, industry TEXT, eps REAL, book_value REAL, current_ratio REAL, quick_ratio REAL, operating_margin REAL, net_margin REAL, cash REAL, free_cash_flow REAL, enterprise_value REAL, beta REAL, week52_high REAL, week52_low REAL, target_price REAL, recommendation TEXT, shares_outstanding REAL);
CREATE TABLE indicators (
    symbol TEXT,
    date TEXT,
    ema20 REAL,
    ema50 REAL, ema200 REAL, sma20 REAL, sma50 REAL, sma200 REAL, rsi REAL, macd REAL, macd_signal REAL, macd_hist REAL, atr REAL, adx REAL, plus_di REAL, minus_di REAL, bb_upper REAL, bb_middle REAL, bb_lower REAL, stochastic_k REAL, stochastic_d REAL, cci REAL, williams_r REAL, obv REAL, vwap REAL, volume_avg20 REAL, breakout_score REAL, swing_score REAL, supertrend REAL, trend TEXT, pivot REAL, cpr_top REAL, cpr_bottom REAL, r1 REAL, r2 REAL, r3 REAL, s1 REAL, s2 REAL, s3 REAL,
    PRIMARY KEY(symbol, date)
);
CREATE TABLE ipo_data (
    symbol TEXT PRIMARY KEY,

    listing_date TEXT,
    listing_price REAL,
    current_price REAL,

    issue_size REAL,
    lot_size INTEGER,

    gmp REAL,

    promoter_holding REAL,
    institutional_holding REAL,

    market_cap REAL,

    volume_ratio REAL,

    below_listing INTEGER,

    updated_at TEXT
);
CREATE TABLE latest_indicators (
    symbol TEXT PRIMARY KEY,
    date TEXT,

    ema20 REAL,
    ema50 REAL,
    ema200 REAL,

    sma20 REAL,
    sma50 REAL,
    sma200 REAL,

    rsi REAL,

    macd REAL,
    macd_signal REAL,
    macd_hist REAL,

    atr REAL,
    adx REAL,
    plus_di REAL,
    minus_di REAL,

    bb_upper REAL,
    bb_middle REAL,
    bb_lower REAL,

    stochastic_k REAL,
    stochastic_d REAL,

    cci REAL,
    williams_r REAL,

    obv REAL,
    vwap REAL,

    volume_avg20 REAL,

    breakout_score REAL,
    swing_score REAL,

    supertrend REAL,
    trend TEXT,

    pivot REAL,
    cpr_top REAL,
    cpr_bottom REAL,

    r1 REAL,
    r2 REAL,
    r3 REAL,

    s1 REAL,
    s2 REAL,
    s3 REAL
, open REAL, high REAL, low REAL, close REAL, volume REAL);
CREATE TABLE update_log (
    process_name TEXT PRIMARY KEY,
    last_run TEXT,
    status TEXT
);
CREATE TABLE dashboard_metrics(

date TEXT PRIMARY KEY,

total_stocks INTEGER,

long_term_buy INTEGER,

swing_buy INTEGER,

smart_money INTEGER,

high_52w_count INTEGER,

high_52w_breakout_count INTEGER,

resistance_breakout_count INTEGER,

support_breakdown_count INTEGER,

pattern_breakout_count INTEGER,

volume_explosion_count INTEGER,

new_listing_count INTEGER,

market_trend TEXT,

top_bullish_stock TEXT,

top_volume_stock TEXT,

last_sync TEXT
);
CREATE TABLE market_signals(

id INTEGER PRIMARY KEY AUTOINCREMENT,

symbol TEXT,

signal_type TEXT,

signal_score REAL,

rank_no INTEGER,

date TEXT
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE "stock_master" (
"symbol" TEXT,
  "company_name" TEXT,
  "exchange" TEXT
);
