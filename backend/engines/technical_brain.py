from typing import Dict

TECHNICAL_WEIGHTS = {
"EMA_ALIGNMENT": 20,
"PRICE_ABOVE_EMA20": 4,
"PRICE_ABOVE_EMA50": 6,
"PRICE_ABOVE_EMA200": 10,
"RSI_STRONG": 10,
"RSI_HEALTHY": 6,
"ADX_STRONG": 10,
"ADX_MODERATE": 6,
"MACD_BULLISH": 8,
"SUPERTREND": 10,
"VWAP": 5,
"HIGH_VOLUME": 10,
"MEDIUM_VOLUME": 5,
"BREAKOUT": 10
}

class TechnicalBrain:

  @staticmethod  
  def _safe(value) -> float:  
    try:  
        if value is None:  
            return 0.0  
        return float(value)  
    except Exception:  
        return 0.0  

  @staticmethod  
  def _ema_analysis(row: Dict):  

    score = 0  
    reasons = []  

    close = TechnicalBrain._safe(row.get("close"))  

    ema20 = TechnicalBrain._safe(row.get("ema20"))  
    ema50 = TechnicalBrain._safe(row.get("ema50"))  
    ema200 = TechnicalBrain._safe(row.get("ema200"))  

    trend = "BEARISH"  

    if ema20 > ema50 > ema200:  

        trend = "STRONG BULLISH"  

        score += TECHNICAL_WEIGHTS["EMA_ALIGNMENT"]  

        reasons.append(  
            "Perfect EMA Alignment"  
        )  

    elif ema20 > ema50:  

        trend = "BULLISH"  

        score += 10  

        reasons.append(  
            "Bullish EMA Structure"  
        )  

    if close > ema20:  

        score += TECHNICAL_WEIGHTS[  
            "PRICE_ABOVE_EMA20"  
        ]  

    if close > ema50:  

        score += TECHNICAL_WEIGHTS[  
            "PRICE_ABOVE_EMA50"  
        ]  

    if close > ema200:  

        score += TECHNICAL_WEIGHTS[  
            "PRICE_ABOVE_EMA200"  
        ]  

    return {  
        "score": score,  
        "trend": trend,  
        "reasons": reasons  
    }  

@staticmethod  
def _rsi_analysis(row: Dict):  

    score = 0  

    reasons = []  

    rsi = TechnicalBrain._safe(  
        row.get("rsi")  
    )  

    state = "WEAK"  

    if rsi >= 70:  

        score += TECHNICAL_WEIGHTS[  
            "RSI_STRONG"  
        ]  

        state = "VERY STRONG"  

        reasons.append(  
            "RSI Above 70"  
        )  

    elif rsi >= 60:  

        score += TECHNICAL_WEIGHTS[  
            "RSI_HEALTHY"  
        ]  

        state = "STRONG"  

        reasons.append(  
            "Healthy RSI"  
        )  

    elif rsi >= 50:  

        score += 3  

        state = "POSITIVE"  

    elif rsi < 40:  

        score -= 8  

        reasons.append(  
            "Weak RSI"  
        )  

    return {  

        "score": score,  

        "state": state,  

        "value": round(rsi, 2),  

        "reasons": reasons  
    }  

@staticmethod  
def _adx_analysis(row: Dict):  

    score = 0  

    reasons = []  

    adx = TechnicalBrain._safe(  
        row.get("adx")  
    )  

    plus_di = TechnicalBrain._safe(  
        row.get("plus_di")  
    )  

    minus_di = TechnicalBrain._safe(  
        row.get("minus_di")  
    )  

    strength = "LOW"  

    if adx >= 35:  

        strength = "VERY STRONG"  

        score += TECHNICAL_WEIGHTS[  
            "ADX_STRONG"  
        ]  

        reasons.append(  
            "Strong Trend"  
        )  

    elif adx >= 25:  

        strength = "STRONG"  

        score += TECHNICAL_WEIGHTS[  
            "ADX_MODERATE"  
        ]  

    elif adx >= 20:  

        strength = "MODERATE"  

        score += 3  

    if plus_di > minus_di:  

        score += 3  

        reasons.append(  
            "Buyers Dominating"  
        )  

    return {  

        "score": score,  

        "strength": strength,  

        "value": round(adx, 2),  

        "reasons": reasons  
    }  
@staticmethod  
def _macd_analysis(row: Dict):  

    score = 0  
    reasons = []  

    macd = TechnicalBrain._safe(row.get("macd"))  
    signal = TechnicalBrain._safe(row.get("macd_signal"))  
    hist = TechnicalBrain._safe(row.get("macd_hist"))  

    state = "BEARISH"  

    if macd > signal:  

        state = "BULLISH"  

        score += TECHNICAL_WEIGHTS[  
            "MACD_BULLISH"  
        ]  

        reasons.append(  
            "MACD Bullish Crossover"  
        )  

        if hist > 0:  

            score += 2  

            reasons.append(  
                "Positive MACD Histogram"  
            )  

    else:  

        score -= 4  

    return {  

        "score": score,  

        "state": state,  

        "histogram": round(hist, 2),  

        "reasons": reasons  
    }  

@staticmethod  
def _supertrend_analysis(row: Dict):  

    score = 0  

    reasons = []  

    close = TechnicalBrain._safe(  
        row.get("close")  
    )  

    supertrend = TechnicalBrain._safe(  
        row.get("supertrend")  
    )  

    signal = "SELL"  

    if close > supertrend:  

        signal = "BUY"  

        score += TECHNICAL_WEIGHTS[  
            "SUPERTREND"  
        ]  

        reasons.append(  
            "Above Supertrend"  
        )  

    else:  

        score -= 8  

    return {  

        "score": score,  

        "signal": signal,  

        "reasons": reasons  
    }  

@staticmethod  
def _vwap_analysis(row: Dict):  

    score = 0  

    reasons = []  

    close = TechnicalBrain._safe(  
        row.get("close")  
    )  

    vwap = TechnicalBrain._safe(  
        row.get("vwap")  
    )  

    signal = "BELOW"  

    if close > vwap:  

        signal = "ABOVE"  

        score += TECHNICAL_WEIGHTS[  
            "VWAP"  
        ]  

        reasons.append(  
            "Trading Above VWAP"  
        )  

    else:  

        score -= 2  

    return {  

        "score": score,  

        "signal": signal,  

        "reasons": reasons  
    }  

@staticmethod  
def _volume_analysis(row: Dict):  

    score = 0  

    reasons = []  

    volume = TechnicalBrain._safe(  
        row.get("volume")  
    )  

    avg_volume = TechnicalBrain._safe(  
        row.get("volume_avg20")  
    )  

    ratio = 0.0  

    if avg_volume > 0:  

        ratio = volume / avg_volume  

    strength = "LOW"  

    if ratio >= 2:  

        strength = "VERY HIGH"  

        score += TECHNICAL_WEIGHTS[  
            "HIGH_VOLUME"  
        ]  

        reasons.append(  
            "Volume Explosion"  
        )  

    elif ratio >= 1.5:  

        strength = "HIGH"  

        score += TECHNICAL_WEIGHTS[  
            "MEDIUM_VOLUME"  
        ]  

        reasons.append(  
            "Strong Buying Volume"  
        )  

    elif ratio >= 1:  

        strength = "NORMAL"  

    else:  

        score -= 2  

    return {  

        "score": score,  

        "ratio": round(ratio, 2),  

        "strength": strength,  

        "reasons": reasons  
    }  

@staticmethod  
def _atr_analysis(row: Dict):  

    atr = TechnicalBrain._safe(  
        row.get("atr")  
    )  

    close = TechnicalBrain._safe(  
        row.get("close")  
    )  

    risk = "HIGH"  

    risk_pct = 0.0  

    if close > 0:  

        risk_pct = (atr / close) * 100  

    if risk_pct <= 2:  

        risk = "LOW"  

    elif risk_pct <= 4:  

        risk = "MEDIUM"  

    return {  

        "atr": round(atr, 2),  

        "risk_percent": round(  
            risk_pct,  
            2  
        ),  

        "risk": risk  
    }  
@staticmethod  
def _support_resistance_analysis(row: Dict):  

    score = 0  
    reasons = []  

    close = TechnicalBrain._safe(row.get("close"))  

    pivot = TechnicalBrain._safe(row.get("pivot"))  

    r1 = TechnicalBrain._safe(row.get("r1"))  
    r2 = TechnicalBrain._safe(row.get("r2"))  
    r3 = TechnicalBrain._safe(row.get("r3"))  

    s1 = TechnicalBrain._safe(row.get("s1"))  
    s2 = TechnicalBrain._safe(row.get("s2"))  
    s3 = TechnicalBrain._safe(row.get("s3"))  

    signal = "NEUTRAL"  

    nearest_support = None  
    nearest_resistance = None  

    supports = [  
        x for x in [s1, s2, s3]  
        if x > 0  
    ]  

    resistances = [  
        x for x in [r1, r2, r3]  
        if x > close  
    ]  

    if supports:  

        nearest_support = max(supports)  

    if resistances:  

        nearest_resistance = min(resistances)  

    if (  
        nearest_resistance  
        and close > nearest_resistance  
    ):  

        signal = "RESISTANCE BREAKOUT"  

        score += 10  

        reasons.append(  
            "Resistance Broken"  
        )  

    elif (  
        nearest_support  
        and close > nearest_support  
    ):  

        score += 4  

        reasons.append(  
            "Trading Above Support"  
        )  

    if close > pivot:  

        score += 2  

    return {  

        "score": score,  

        "signal": signal,  

        "pivot": round(pivot, 2),  

        "nearest_support":  
            nearest_support,  

        "nearest_resistance":  
            nearest_resistance,  

        "reasons": reasons  
    }  

@staticmethod  
def _breakout_analysis(row: Dict):  

    score = 0  

    reasons = []  

    breakout = TechnicalBrain._safe(  
        row.get("breakout_score")  
    )  

    signal = "NONE"  

    if breakout >= 80:  

        signal = "STRONG"  

        score += 10  

        reasons.append(  
            "High Probability Breakout"  
        )  

    elif breakout >= 60:  

        signal = "MODERATE"  

        score += 6  

        reasons.append(  
            "Potential Breakout"  
        )  

    elif breakout >= 40:  

        signal = "WATCH"  

        score += 2  

    return {  

        "score": score,  

        "signal": signal,  

        "breakout_score":  
            breakout,  

        "reasons": reasons  
    }  

@staticmethod  
def _momentum_analysis(row: Dict):  

    score = 0  

    reasons = []  

    rsi = TechnicalBrain._safe(  
        row.get("rsi")  
    )  

    adx = TechnicalBrain._safe(  
        row.get("adx")  
    )  

    macd = TechnicalBrain._safe(  
        row.get("macd")  
    )  

    signal = TechnicalBrain._safe(  
        row.get("macd_signal")  
    )  

    state = "WEAK"  

    if (  
        rsi >= 60  
        and adx >= 25  
        and macd > signal  
    ):  

        state = "STRONG"  

        score += 15  

        reasons.append(  
            "Momentum Confirmed"  
        )  

    elif (  
        rsi >= 50  
    ):  

        state = "MODERATE"  

        score += 8  

    return {  

        "score": score,  

        "state": state,  

        "reasons": reasons  
    }  

@staticmethod  
def _volatility_analysis(row: Dict):  

    score = 0  

    reasons = []  

    atr = TechnicalBrain._safe(  
        row.get("atr")  
    )  

    close = TechnicalBrain._safe(  
        row.get("close")  
    )  

    state = "HIGH"  

    volatility = 0  

    if close > 0:  

        volatility = (  
            atr / close  
        ) * 100  

    if volatility <= 2:  

        state = "LOW"  

        score += 6  

        reasons.append(  
            "Low Volatility"  
        )  

    elif volatility <= 4:  

        state = "MEDIUM"  

        score += 3  

    else:  

        score -= 2  

        reasons.append(  
            "High Volatility"  
        )  

    return {  

        "score": score,  

        "volatility":  
            round(volatility, 2),  

        "state": state,  

        "reasons": reasons  
    }  

@staticmethod  
def _confidence(score: float):  

    return max(  
        0,  
        min(  
            100,  
            round(score)  
        )  
    )  
@staticmethod  
def analyze(row: Dict):  

    ema = TechnicalBrain._ema_analysis(row)  

    rsi = TechnicalBrain._rsi_analysis(row)  

    adx = TechnicalBrain._adx_analysis(row)  

    macd = TechnicalBrain._macd_analysis(row)  

    supertrend = TechnicalBrain._supertrend_analysis(row)  

    vwap = TechnicalBrain._vwap_analysis(row)  

    volume = TechnicalBrain._volume_analysis(row)  

    atr = TechnicalBrain._atr_analysis(row)  

    support = TechnicalBrain._support_resistance_analysis(row)  

    breakout = TechnicalBrain._breakout_analysis(row)  

    momentum = TechnicalBrain._momentum_analysis(row)  

    volatility = TechnicalBrain._volatility_analysis(row)  

    total = (  
        ema["score"]  
        + rsi["score"]  
        + adx["score"]  
        + macd["score"]  
        + supertrend["score"]  
        + vwap["score"]  
        + volume["score"]  
        + support["score"]  
        + breakout["score"]  
        + momentum["score"]  
        + volatility["score"]  
    )  

    total = max(  
        0,  
        min(  
            100,  
            round(total, 2)  
        )  
    )  

    confidence = TechnicalBrain._confidence(  
        total  
    )  

    signal = "SELL"  

    allocation = 0  

    if total >= 90:  

        signal = "STRONG BUY"  

        allocation = 20  

    elif total >= 80:  

        signal = "BUY"  

        allocation = 15  

    elif total >= 65:  

        signal = "ACCUMULATE"  

        allocation = 10  

    elif total >= 50:  

        signal = "HOLD"  

    else:  

        signal = "SELL"  

    reasons = []  

    for engine in [  

        ema,  

        rsi,  

        adx,  

        macd,  

        supertrend,  

        vwap,  

        volume,  

        support,  

        breakout,  

        momentum,  

        volatility  

    ]:  

        reasons.extend(  
            engine["reasons"]  
        )  

    reasons = list(  
        dict.fromkeys(reasons)  
    )  

    return {  

        "technical_score": total,  

        "technical_signal": signal,  

        "confidence": confidence,  

        "allocation": allocation,  

        "trend": ema["trend"],  

        "momentum": momentum["state"],  

        "volume_strength":  
            volume["strength"],  

        "volume_ratio":  
            volume["ratio"],  

        "breakout":  
            breakout["signal"],  

        "breakout_score":  
            breakout["breakout_score"],  

        "nearest_support":  
            support["nearest_support"],  

        "nearest_resistance":  
            support["nearest_resistance"],  

        "pivot":  
            support["pivot"],  

        "volatility":  
            volatility["volatility"],  

        "volatility_state":  
            volatility["state"],  

        "atr":  
            atr["atr"],  

        "risk":  
            atr["risk"],  

        "risk_percent":  
            atr["risk_percent"],  

        "reasons": reasons  
    }
