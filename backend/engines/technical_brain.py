# ============================================================
# FILE: backend/engines/technical_brain.py
# PART-01
# ============================================================

from typing import Dict, List


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
    def _pct_change(a: float, b: float) -> float:

        if b == 0:

            return 0.0

        return ((a - b) / b) * 100

    @staticmethod
    def _slope(values: List[float]) -> float:

        if len(values) < 2:

            return 0.0

        return values[-1] - values[0]

    @staticmethod
    def _highest(values: List[float]) -> float:

        if not values:

            return 0.0

        return max(values)

    @staticmethod
    def _lowest(values: List[float]) -> float:

        if not values:

            return 0.0

        return min(values)

    @staticmethod
    def _avg(values: List[float]) -> float:

        if not values:

            return 0.0

        return sum(values) / len(values)

    @staticmethod
    def _load_series(
        history: List[Dict],
        key: str
    ) -> List[float]:

        series = []

        for row in history:

            series.append(

                TechnicalBrain._safe(

                    row.get(key)

                )

            )

        return series

    @staticmethod
    def _trend_context(
        latest: Dict,
        history: List[Dict]
    ):

        close = TechnicalBrain._safe(
            latest.get("close")
        )

        low = TechnicalBrain._safe(
            latest.get("low")
        )

        ema20 = TechnicalBrain._load_series(
            history,
            "ema20"
        )

        ema50 = TechnicalBrain._load_series(
            history,
            "ema50"
        )

        ema200 = TechnicalBrain._load_series(
            history,
            "ema200"
        )

        current20 = ema20[-1]
        current50 = ema50[-1]
        current200 = ema200[-1]

        score = 0

        trend = "SIDEWAYS"

        health = "WEAK"

        pullback = "NONE"

        reasons = []

        if current20 > current50 > current200:

            trend = "STRONG_BULLISH"

            score += 20

            reasons.append(
                "Perfect EMA Alignment"
            )

        elif current20 > current50:

            trend = "BULLISH"

            score += 10

            reasons.append(
                "Bullish EMA Structure"
            )

        elif current20 < current50 < current200:

            trend = "STRONG_BEARISH"

            score -= 20

            reasons.append(
                "Bearish EMA Structure"
            )

        slope20 = TechnicalBrain._slope(
            ema20[-10:]
        )

        slope50 = TechnicalBrain._slope(
            ema50[-10:]
        )

        slope200 = TechnicalBrain._slope(
            ema200[-20:]
        )

        if (

            slope20 > 0

            and

            slope50 > 0

            and

            slope200 > 0

        ):

            score += 10

            health = "HEALTHY"

            reasons.append(
                "EMA Slopes Rising"
            )

        distance2050 = abs(
            current20 -
            current50
        )

        previous2050 = abs(
            ema20[-2] -
            ema50[-2]
        )

        expansion = False

        if distance2050 > previous2050:

            expansion = True

            score += 5

            reasons.append(
                "EMA Expansion"
            )

        compression = False

        if distance2050 < 0.50:

            compression = True

            reasons.append(
                "EMA Compression"
            )

        if (

            close >= current20 * 0.995

            and

            close <= current20 * 1.01

        ):

            pullback = "EMA20"

            score += 5

            reasons.append(
                "Healthy EMA20 Pullback"
            )

        elif (

            close >= current50 * 0.995

            and

            close <= current50 * 1.01

        ):

            pullback = "EMA50"

            score += 3

            reasons.append(
                "Deep EMA50 Pullback"
            )

        rejection = False

        if (

            low < current20

            and

            close > current20

        ):

            rejection = True

            score += 4

            reasons.append(
                "EMA20 Rejection"
            )

        return {

            "score": score,

            "trend": trend,

            "health": health,

            "expansion": expansion,

            "compression": compression,

            "pullback": pullback,

            "rejection": rejection,

            "slope20": slope20,

            "slope50": slope50,

            "slope200": slope200,

            "distance2050": distance2050,

            "reasons": reasons

        }

    @staticmethod
    def _momentum_context(
        latest: Dict,
        history: List[Dict]
    ):

        rsi = TechnicalBrain._load_series(
            history,
            "rsi"
        )

        adx = TechnicalBrain._load_series(
            history,
            "adx"
        )

        macd = TechnicalBrain._load_series(
            history,
            "macd"
        )

        signal = TechnicalBrain._load_series(
            history,
            "macd_signal"
        )

        current_rsi = rsi[-1]

        current_adx = adx[-1]

        current_macd = macd[-1]

        current_signal = signal[-1]

        score = 0

        momentum = "WEAK"

        reasons = []

        rsi_slope = TechnicalBrain._slope(
            rsi[-10:]
        )

        adx_slope = TechnicalBrain._slope(
            adx[-10:]
        )

        histogram = current_macd - current_signal

        if (

            current_rsi >= 55

            and

            rsi_slope > 0

        ):

            score += 8

            momentum = "BUILDING"

            reasons.append(
                "RSI Rising"
            )

        if (

            current_rsi >= 60

            and

            rsi_slope > 0

            and

            current_adx >= 20

        ):

            score += 10

            momentum = "STRONG"

            reasons.append(
                "Momentum Expansion"
            )

        if (

            current_rsi >= 70

            and

            rsi_slope < 0

        ):

            score -= 5

            reasons.append(
                "RSI Losing Momentum"
            )

        if current_adx >= 25:

            score += 8

            reasons.append(
                "Strong Trend"
            )

        elif current_adx >= 20:

            score += 4

            reasons.append(
                "Trend Developing"
            )

        if adx_slope > 0:

            score += 3

            reasons.append(
                "ADX Rising"
            )

        if histogram > 0:

            score += 5

            reasons.append(
                "Positive MACD Histogram"
            )

        if (

            current_macd >

            current_signal

        ):

            score += 6

            reasons.append(
                "MACD Bullish"
            )

        divergence = "NONE"

        recent_close = TechnicalBrain._load_series(
            history,
            "close"
        )[-5:]

        recent_rsi = rsi[-5:]

        if (

            recent_close[-1] > recent_close[0]

            and

            recent_rsi[-1] < recent_rsi[0]

        ):

            divergence = "BEARISH"

            score -= 8

            reasons.append(
                "Bearish RSI Divergence"
            )

        elif (

            recent_close[-1] < recent_close[0]

            and

            recent_rsi[-1] > recent_rsi[0]

        ):

            divergence = "BULLISH"

            score += 8

            reasons.append(
                "Bullish RSI Divergence"
            )

        return {

            "score": score,

            "momentum": momentum,

            "divergence": divergence,

            "rsi": current_rsi,

            "adx": current_adx,

            "macd": current_macd,

            "histogram": histogram,

            "reasons": reasons

      }

    @staticmethod
    def _volume_context(
        latest: Dict,
        history: List[Dict]
    ):

        volumes = TechnicalBrain._load_series(
            history,
            "volume"
        )

        closes = TechnicalBrain._load_series(
            history,
            "close"
        )

        current_volume = volumes[-1]

        avg20 = TechnicalBrain._avg(
            volumes[-20:]
        )

        ratio = 0.0

        if avg20 > 0:

            ratio = current_volume / avg20

        score = 0

        strength = "LOW"

        reasons = []

        if ratio >= 2.5:

            strength = "EXTREME"

            score += 12

            reasons.append(
                "Volume Explosion"
            )

        elif ratio >= 2.0:

            strength = "VERY_HIGH"

            score += 10

            reasons.append(
                "Institutional Volume"
            )

        elif ratio >= 1.5:

            strength = "HIGH"

            score += 7

            reasons.append(
                "High Relative Volume"
            )

        elif ratio >= 1.2:

            strength = "ABOVE_AVERAGE"

            score += 4

        else:

            strength = "LOW"

        volume_slope = TechnicalBrain._slope(
            volumes[-10:]
        )

        if volume_slope > 0:

            score += 3

            reasons.append(
                "Volume Increasing"
            )

        candle_change = TechnicalBrain._pct_change(

            closes[-1],

            closes[-2]

        )

        activity = "NORMAL"

        if (

            candle_change > 2

            and

            ratio > 1.5

        ):

            activity = "ACCUMULATION"

            score += 8

            reasons.append(
                "Strong Buying Pressure"
            )

        elif (

            candle_change < -2

            and

            ratio > 1.5

        ):

            activity = "DISTRIBUTION"

            score -= 8

            reasons.append(
                "Strong Selling Pressure"
            )

        elif (

            abs(candle_change) < 0.5

            and

            ratio > 2

        ):

            activity = "ABSORPTION"

            score += 4

            reasons.append(
                "Supply Absorption"
            )

        dry_volume = False

        if ratio < 0.70:

            dry_volume = True

            reasons.append(
                "Dry Volume"
            )

        return {

            "score": score,

            "strength": strength,

            "activity": activity,

            "volume_ratio": round(
                ratio,
                2
            ),

            "volume_slope": round(
                volume_slope,
                2
            ),

            "dry_volume": dry_volume,

            "reasons": reasons

        }

    @staticmethod
    def _breakout_context(
        latest: Dict,
        history: List[Dict]
    ):

        closes = TechnicalBrain._load_series(
            history,
            "close"
        )

        highs = TechnicalBrain._load_series(
            history,
            "high"
        )

        lows = TechnicalBrain._load_series(
            history,
            "low"
        )

        volumes = TechnicalBrain._load_series(
            history,
            "volume"
        )

        close = closes[-1]

        high20 = max(highs[-20:])
        low20 = min(lows[-20:])

        avg_volume = TechnicalBrain._avg(
            volumes[-20:]
        )

        volume_ratio = 0.0

        if avg_volume > 0:

            volume_ratio = (

                volumes[-1] /

                avg_volume

            )

        score = 0

        breakout = "NONE"

        breakout_strength = 0

        fakeout = False

        reasons = []

        if (

            close >= high20 * 0.995

        ):

            breakout = "NEAR_BREAKOUT"

            score += 5

            reasons.append(
                "Near 20-Day High"
            )

        if (

            close > high20

            and

            volume_ratio >= 1.5

        ):

            breakout = "CONFIRMED"

            breakout_strength = 90

            score += 15

            reasons.append(
                "Volume Confirmed Breakout"
            )

        elif (

            close > high20

        ):

            breakout = "WEAK"

            breakout_strength = 60

            score += 8

            reasons.append(
                "Low Volume Breakout"
            )

        if (

            close < high20

            and

            volumes[-1] >

            avg_volume * 2

        ):

            fakeout = True

            breakout = "FAILED"

            breakout_strength = 20

            score -= 10

            reasons.append(
                "Failed Breakout"
            )

        support_distance = 0.0

        resistance_distance = 0.0

        if close > 0:

            support_distance = (

                (

                    close -

                    low20

                )

                /

                close

            ) * 100

            resistance_distance = (

                (

                    high20 -

                    close

                )

                /

                close

            ) * 100

        return {

            "score": score,

            "breakout": breakout,

            "breakout_strength":

                breakout_strength,

            "fakeout":

                fakeout,

            "support_distance":

                round(

                    support_distance,

                    2

                ),

            "resistance_distance":

                round(

                    resistance_distance,

                    2

                ),

            "reasons":

                reasons

        }

    @staticmethod
    def _risk_context(
        latest: Dict,
        history: List[Dict]
    ):

        atr = TechnicalBrain._safe(
            latest.get("atr")
        )

        close = TechnicalBrain._safe(
            latest.get("close")
        )

        rsi = TechnicalBrain._safe(
            latest.get("rsi")
        )

        adx = TechnicalBrain._safe(
            latest.get("adx")
        )

        volume = TechnicalBrain._safe(
            latest.get("volume")
        )

        avg_volume = TechnicalBrain._safe(
            latest.get("volume_avg20")
        )

        score = 0

        risk = "HIGH"

        reasons = []

        atr_percent = 0.0

        if close > 0:

            atr_percent = (

                atr / close

            ) * 100

        if atr_percent <= 2:

            risk = "LOW"

            score += 10

            reasons.append(
                "Controlled Volatility"
            )

        elif atr_percent <= 4:

            risk = "MEDIUM"

            score += 5

            reasons.append(
                "Healthy Volatility"
            )

        else:

            score -= 5

            reasons.append(
                "High Volatility"
            )

        volume_ratio = 0.0

        if avg_volume > 0:

            volume_ratio = (

                volume /

                avg_volume

            )

        if (

            rsi >= 60

            and

            adx >= 25

            and

            volume_ratio >= 1.5

        ):

            score += 8

            reasons.append(
                "Trend Risk Reduced"
            )

        if (

            rsi >= 75

            and

            atr_percent >= 5

        ):

            score -= 10

            reasons.append(
                "Overheated Move"
            )

        probability = max(

            0,

            min(

                100,

                50 + score

            )

        )

        return {

            "score": score,

            "risk": risk,

            "risk_probability":

                probability,

            "atr_percent":

                round(

                    atr_percent,

                    2

                ),

            "volume_ratio":

                round(

                    volume_ratio,

                    2

                ),

            "reasons":

                reasons

        }

    @staticmethod
    def _risk_context(
        latest: Dict,
        history: List[Dict]
    ):

        close = TechnicalBrain._safe(
            latest.get("close")
        )

        atr = TechnicalBrain._safe(
            latest.get("atr")
        )

        vwap = TechnicalBrain._safe(
            latest.get("vwap")
        )

        score = 0

        risk = "HIGH"

        volatility = 0.0

        reasons = []

        if close > 0:

            volatility = (

                atr /

                close

            ) * 100

        if volatility <= 2:

            risk = "LOW"

            score += 8

            reasons.append(
                "Low Volatility"
            )

        elif volatility <= 4:

            risk = "MEDIUM"

            score += 4

            reasons.append(
                "Controlled Volatility"
            )

        else:

            risk = "HIGH"

            score -= 5

            reasons.append(
                "High Volatility"
            )

        vwap_signal = "BELOW"

        if close > vwap:

            vwap_signal = "ABOVE"

            score += 5

            reasons.append(
                "Trading Above VWAP"
            )

        highs = TechnicalBrain._load_series(
            history,
            "high"
        )

        lows = TechnicalBrain._load_series(
            history,
            "low"
        )

        support = min(
            lows[-20:]
        )

        resistance = max(
            highs[-20:]
        )

        support_gap = 0.0

        resistance_gap = 0.0

        if close > 0:

            support_gap = (

                (

                    close -

                    support

                )

                /

                close

            ) * 100

            resistance_gap = (

                (

                    resistance -

                    close

                )

                /

                close

            ) * 100

        rr = 0.0

        if support_gap > 0:

            rr = resistance_gap / support_gap

        rr_quality = "POOR"

        if rr >= 3:

            rr_quality = "EXCELLENT"

            score += 8

            reasons.append(
                "Excellent Risk Reward"
            )

        elif rr >= 2:

            rr_quality = "GOOD"

            score += 5

            reasons.append(
                "Good Risk Reward"
            )

        elif rr >= 1:

            rr_quality = "AVERAGE"

            score += 2

        else:

            rr_quality = "POOR"

            score -= 4

            reasons.append(
                "Poor Risk Reward"
            )

        return {

            "score": score,

            "risk": risk,

            "volatility":

                round(
                    volatility,
                    2
                ),

            "vwap":

                vwap_signal,

            "support":

                round(
                    support,
                    2
                ),

            "resistance":

                round(
                    resistance,
                    2
                ),

            "support_gap":

                round(
                    support_gap,
                    2
                ),

            "resistance_gap":

                round(
                    resistance_gap,
                    2
                ),

            "risk_reward":

                round(
                    rr,
                    2
                ),

            "rr_quality":

                rr_quality,

            "reasons":

                reasons

              }

    @staticmethod
    def analyze(
        latest: Dict,
        history: List[Dict]
    ):

        if len(history) < 30:

            return {

                "technical_score": 0,

                "technical_signal": "UNKNOWN",

                "confidence": 0,

                "reasons": [

                    "Insufficient Historical Data"

                ]

            }

        trend = TechnicalBrain._trend_context(

            latest,

            history

        )

        momentum = TechnicalBrain._momentum_context(

            latest,

            history

        )

        volume = TechnicalBrain._volume_context(

            latest,

            history

        )

        breakout = TechnicalBrain._breakout_context(

            latest,

            history

        )

        risk = TechnicalBrain._risk_context(

            latest,

            history

        )

        score = (

            trend["score"]

            +

            momentum["score"]

            +

            volume["score"]

            +

            breakout["score"]

            +

            risk["score"]

        )

        score = max(

            0,

            min(

                100,

                round(score)

            )

        )

        confidence = 45

        confidence += trend["score"] // 2

        confidence += momentum["score"] // 2

        confidence += volume["score"] // 2

        confidence += breakout["score"] // 2

        confidence = max(

            0,

            min(

                100,

                confidence

            )

        )

        signal = "SELL"

        allocation = 0

        if score >= 85:

            signal = "STRONG BUY"

            allocation = 20

        elif score >= 70:

            signal = "BUY"

            allocation = 15

        elif score >= 55:

            signal = "ACCUMULATE"

            allocation = 10

        elif score >= 45:

            signal = "HOLD"

        reasons = []

        for engine in [

            trend,

            momentum,

            volume,

            breakout,

            risk

        ]:

            reasons.extend(

                engine["reasons"]

            )

        reasons = list(

            dict.fromkeys(

                reasons

            )

        )

        return {

            "technical_score":

                score,

            "technical_signal":

                signal,

            "confidence":

                confidence,

            "allocation":

                allocation,

            "trend":

                trend["trend"],

            "trend_health":

                trend["health"],

            "momentum":

                momentum["momentum"],

            "volume_strength":

                volume["strength"],

            "volume_activity":

                volume["activity"],

            "volume_ratio":

                volume["volume_ratio"],

            "breakout":

                breakout["breakout"],

            "breakout_strength":

                breakout["breakout_strength"],

            "fakeout":

                breakout["fakeout"],

            "risk":

                risk["risk"],

            "risk_reward":

                risk["risk_reward"],

            "rr_quality":

                risk["rr_quality"],

            "support":

                risk["support"],

            "resistance":

                risk["resistance"],

            "reasons":

                reasons

        }

  # ============================================================
# ADD THESE METHODS INSIDE class TechnicalBrain
# FILE: backend/engines/technical_brain.py
# ============================================================

    @staticmethod
    def _market_structure_context(
        history: List[Dict]
    ):

        highs = TechnicalBrain._load_series(
            history,
            "high"
        )

        lows = TechnicalBrain._load_series(
            history,
            "low"
        )

        closes = TechnicalBrain._load_series(
            history,
            "close"
        )

        score = 0

        structure = "RANGE"

        reasons = []

        hh = 0
        hl = 0
        lh = 0
        ll = 0

        for i in range(1, len(highs)):

            if highs[i] > highs[i - 1]:
                hh += 1
            else:
                lh += 1

            if lows[i] > lows[i - 1]:
                hl += 1
            else:
                ll += 1

        if hh >= 12 and hl >= 12:

            structure = "UPTREND"

            score += 15

            reasons.append(
                "Higher High Higher Low"
            )

        elif lh >= 12 and ll >= 12:

            structure = "DOWNTREND"

            score -= 15

            reasons.append(
                "Lower High Lower Low"
            )

        else:

            structure = "RANGE"

            reasons.append(
                "Sideways Structure"
            )

        bos = False

        if closes[-1] > max(highs[-6:-1]):

            bos = True

            score += 6

            reasons.append(
                "Bullish BOS"
            )

        choch = False

        if (

            closes[-1] < lows[-2]

            and

            structure == "UPTREND"

        ):

            choch = True

            score -= 8

            reasons.append(
                "Possible CHOCH"
            )

        return {

            "score": score,

            "structure": structure,

            "bos": bos,

            "choch": choch,

            "higher_highs": hh,

            "higher_lows": hl,

            "lower_highs": lh,

            "lower_lows": ll,

            "reasons": reasons

        }

    @staticmethod
    def _decision_context(
        trend,
        momentum,
        volume,
        breakout,
        structure,
        risk
    ):

        score = (

            trend["score"]

            +

            momentum["score"]

            +

            volume["score"]

            +

            breakout["score"]

            +

            structure["score"]

            +

            risk["score"]

        )

        score = max(
            0,
            min(
                100,
                round(score)
            )
        )

        confidence = score

        if (

            structure["bos"]

            and

            breakout["breakout"] == "CONFIRMED"

        ):

            confidence += 5

        confidence = min(
            100,
            confidence
        )

        signal = "SELL"

        allocation = 0

        if score >= 90:

            signal = "STRONG BUY"

            allocation = 20

        elif score >= 80:

            signal = "BUY"

            allocation = 15

        elif score >= 65:

            signal = "ACCUMULATE"

            allocation = 10

        elif score >= 50:

            signal = "HOLD"

        reasons = []

        for engine in [

            trend,

            momentum,

            volume,

            breakout,

            structure,

            risk

        ]:

            reasons.extend(

                engine["reasons"]

            )

        reasons = list(

            dict.fromkeys(

                reasons

            )

        )

        return {

            "technical_score": score,

            "technical_signal": signal,

            "confidence": confidence,

            "allocation": allocation,

            "reasons": reasons

        }

  # ============================================================
# REPLACE analyze()
# FILE: backend/engines/technical_brain.py
# ============================================================

    @staticmethod
    def analyze(
        latest: Dict,
        history: List[Dict]
    ):

        if len(history) < 30:

            return {

                "technical_score": 0,

                "technical_signal": "UNKNOWN",

                "confidence": 0,

                "allocation": 0,

                "reasons": [

                    "Insufficient Historical Data"

                ]

            }

        trend = TechnicalBrain._trend_context(

            latest,
            history

        )

        momentum = TechnicalBrain._momentum_context(

            latest,
            history

        )

        volume = TechnicalBrain._volume_context(

            latest,
            history

        )

        breakout = TechnicalBrain._breakout_context(

            latest,
            history

        )

        structure = TechnicalBrain._market_structure_context(

            history

        )

        risk = TechnicalBrain._risk_context(

            latest,
            history

        )

        decision = TechnicalBrain._decision_context(

            trend,

            momentum,

            volume,

            breakout,

            structure,

            risk

        )

        return {

            **decision,

            "trend":

                trend["trend"],

            "trend_health":

                trend["health"],

            "ema_expansion":

                trend["expansion"],

            "ema_compression":

                trend["compression"],

            "pullback":

                trend["pullback"],

            "ema_rejection":

                trend["rejection"],

            "ema20_slope":

                round(

                    trend["slope20"],

                    3

                ),

            "ema50_slope":

                round(

                    trend["slope50"],

                    3

                ),

            "ema200_slope":

                round(

                    trend["slope200"],

                    3

                ),

            "momentum":

                momentum["momentum"],

            "rsi":

                round(

                    momentum["rsi"],

                    2

                ),

            "adx":

                round(

                    momentum["adx"],

                    2

                ),

            "macd":

                round(

                    momentum["macd"],

                    3

                ),

            "macd_histogram":

                round(

                    momentum["histogram"],

                    3

                ),

            "divergence":

                momentum["divergence"],

            "volume_strength":

                volume["strength"],

            "volume_activity":

                volume["activity"],

            "volume_ratio":

                volume["volume_ratio"],

            "breakout":

                breakout["breakout"],

            "breakout_strength":

                breakout["breakout_strength"],

            "fakeout":

                breakout["fakeout"],

            "support_distance":

                breakout["support_distance"],

            "resistance_distance":

                breakout["resistance_distance"],

            "market_structure":

                structure["structure"],

            "bos":

                structure["bos"],

            "choch":

                structure["choch"],

            "higher_highs":

                structure["higher_highs"],

            "higher_lows":

                structure["higher_lows"],

            "lower_highs":

                structure["lower_highs"],

            "lower_lows":

                structure["lower_lows"],

            "risk":

                risk["risk"],

            "volatility":

                risk["volatility"],

            "vwap_position":

                risk["vwap"],

            "risk_reward":

                risk["risk_reward"],

            "rr_quality":

                risk["rr_quality"],

            "support":

                risk["support"],

            "resistance":

                risk["resistance"]

        }

  # ============================================================
# ADD THESE METHODS INSIDE class TechnicalBrain
# FILE: backend/engines/technical_brain.py
# ============================================================

    @staticmethod
    def _institutional_context(
        latest: Dict,
        history: List[Dict]
    ):

        delivery = TechnicalBrain._safe(
            latest.get("delivery_percent")
        )

        fii = TechnicalBrain._safe(
            latest.get("fii_change")
        )

        dii = TechnicalBrain._safe(
            latest.get("dii_change")
        )

        oi = TechnicalBrain._safe(
            latest.get("oi_change")
        )

        score = 0

        activity = "NEUTRAL"

        reasons = []

        if delivery >= 55:

            score += 8

            reasons.append(
                "High Delivery Buying"
            )

        elif delivery >= 40:

            score += 4

        if fii > 0:

            score += 6

            reasons.append(
                "FII Buying"
            )

        elif fii < 0:

            score -= 6

            reasons.append(
                "FII Selling"
            )

        if dii > 0:

            score += 4

            reasons.append(
                "DII Buying"
            )

        if oi > 5:

            score += 5

            reasons.append(
                "Open Interest Increasing"
            )

        if score >= 15:

            activity = "STRONG_ACCUMULATION"

        elif score >= 8:

            activity = "ACCUMULATION"

        elif score <= -5:

            activity = "DISTRIBUTION"

        return {

            "score": score,

            "activity": activity,

            "delivery": delivery,

            "fii": fii,

            "dii": dii,

            "oi": oi,

            "reasons": reasons

        }


    @staticmethod
    def _entry_context(
        latest: Dict,
        history: List[Dict]
    ):

        close = TechnicalBrain._safe(
            latest.get("close")
        )

        atr = TechnicalBrain._safe(
            latest.get("atr")
        )

        high = max(

            TechnicalBrain._load_series(

                history[-20:],

                "high"

            )

        )

        low = min(

            TechnicalBrain._load_series(

                history[-20:],

                "low"

            )

        )

        buy = round(
            close,
            2
        )

        stop = round(
            close - atr,
            2
        )

        target1 = round(
            close + atr * 2,
            2
        )

        target2 = round(
            close + atr * 4,
            2
        )

        breakout_entry = round(
            high * 1.002,
            2
        )

        swing_support = round(
            low,
            2
        )

        return {

            "buy_price": buy,

            "breakout_entry":
                breakout_entry,

            "stop_loss":
                stop,

            "target1":
                target1,

            "target2":
                target2,

            "swing_support":
                swing_support

        }

  # ============================================================
# UPDATE analyze()
# FILE: backend/engines/technical_brain.py
# ============================================================

        institution = TechnicalBrain._institutional_context(

            latest,

            history

        )

        entry = TechnicalBrain._entry_context(

            latest,

            history

        )

        decision = TechnicalBrain._decision_context(

            trend,

            momentum,

            volume,

            breakout,

            structure,

            risk

        )

        decision["technical_score"] = max(

            0,

            min(

                100,

                decision["technical_score"]

                +

                institution["score"]

            )

        )

        decision["confidence"] = max(

            0,

            min(

                100,

                decision["confidence"]

                +

                max(

                    0,

                    institution["score"] // 2

                )

            )

        )

        return {

            **decision,

            "trend":
                trend["trend"],

            "trend_health":
                trend["health"],

            "ema_expansion":
                trend["expansion"],

            "ema_compression":
                trend["compression"],

            "pullback":
                trend["pullback"],

            "ema_rejection":
                trend["rejection"],

            "ema20_slope":
                round(
                    trend["slope20"],
                    3
                ),

            "ema50_slope":
                round(
                    trend["slope50"],
                    3
                ),

            "ema200_slope":
                round(
                    trend["slope200"],
                    3
                ),

            "momentum":
                momentum["momentum"],

            "divergence":
                momentum["divergence"],

            "rsi":
                round(
                    momentum["rsi"],
                    2
                ),

            "adx":
                round(
                    momentum["adx"],
                    2
                ),

            "macd":
                round(
                    momentum["macd"],
                    3
                ),

            "histogram":
                round(
                    momentum["histogram"],
                    3
                ),

            "volume_strength":
                volume["strength"],

            "volume_activity":
                volume["activity"],

            "volume_ratio":
                volume["volume_ratio"],

            "breakout":
                breakout["breakout"],

            "breakout_strength":
                breakout["breakout_strength"],

            "fakeout":
                breakout["fakeout"],

            "market_structure":
                structure["structure"],

            "bos":
                structure["bos"],

            "choch":
                structure["choch"],

            "risk":
                risk["risk"],

            "risk_reward":
                risk["risk_reward"],

            "rr_quality":
                risk["rr_quality"],

            "support":
                risk["support"],

            "resistance":
                risk["resistance"],

            "institutional_activity":
                institution["activity"],

            "delivery":
                institution["delivery"],

            "fii_change":
                institution["fii"],

            "dii_change":
                institution["dii"],

            "oi_change":
                institution["oi"],

            "buy_price":
                entry["buy_price"],

            "breakout_entry":
                entry["breakout_entry"],

            "stop_loss":
                entry["stop_loss"],

            "target1":
                entry["target1"],

            "target2":
                entry["target2"],

            "swing_support":
                entry["swing_support"]

        }

  # ============================================================
# ADD THESE METHODS INSIDE class TechnicalBrain
# FILE: backend/engines/technical_brain.py
# ============================================================

    @staticmethod
    def _ai_reasoning(
        trend,
        momentum,
        volume,
        breakout,
        structure,
        institution,
        risk
    ):

        reasons = []

        positives = []

        negatives = []

        if trend["trend"] == "STRONG_BULLISH":

            positives.append(
                "Primary trend is strongly bullish."
            )

        elif trend["trend"] == "BULLISH":

            positives.append(
                "Primary trend remains bullish."
            )

        else:

            negatives.append(
                "Trend is weak."
            )

        if momentum["momentum"] == "STRONG":

            positives.append(
                "Momentum is expanding."
            )

        elif momentum["momentum"] == "BUILDING":

            positives.append(
                "Momentum is building."
            )

        if momentum["divergence"] == "BEARISH":

            negatives.append(
                "Bearish divergence detected."
            )

        elif momentum["divergence"] == "BULLISH":

            positives.append(
                "Bullish divergence detected."
            )

        if volume["activity"] == "ACCUMULATION":

            positives.append(
                "Volume confirms accumulation."
            )

        elif volume["activity"] == "DISTRIBUTION":

            negatives.append(
                "Distribution pressure detected."
            )

        elif volume["activity"] == "ABSORPTION":

            positives.append(
                "Supply absorption visible."
            )

        if breakout["breakout"] == "CONFIRMED":

            positives.append(
                "Breakout confirmed by price."
            )

        elif breakout["fakeout"]:

            negatives.append(
                "Possible fake breakout."
            )

        if structure["bos"]:

            positives.append(
                "Bullish Break Of Structure."
            )

        if structure["choch"]:

            negatives.append(
                "Possible Change Of Character."
            )

        if institution["activity"] in (

            "ACCUMULATION",

            "STRONG_ACCUMULATION"

        ):

            positives.append(
                "Institutional buying detected."
            )

        elif institution["activity"] == "DISTRIBUTION":

            negatives.append(
                "Institutional selling pressure."
            )

        if risk["risk"] == "LOW":

            positives.append(
                "Volatility remains controlled."
            )

        elif risk["risk"] == "HIGH":

            negatives.append(
                "Risk is elevated."
            )

        reasons.extend(positives)

        reasons.extend(negatives)

        verdict = "NEUTRAL"

        if len(positives) >= 6:

            verdict = "HIGH_PROBABILITY_LONG"

        elif len(positives) >= 4:

            verdict = "LONG"

        elif len(negatives) >= 5:

            verdict = "AVOID"

        return {

            "verdict": verdict,

            "positives": positives,

            "negatives": negatives,

            "reasoning": reasons

        }
