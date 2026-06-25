from typing import Dict, List
from statistics import mean


class TrendEngine:

    @staticmethod
    def _safe(value):

        try:

            if value is None:
                return 0.0

            return float(value)

        except:

            return 0.0

    @staticmethod
    def _ema_distance(a, b):

        return abs(a - b)

    @staticmethod
    def _slope(values):

        if len(values) < 5:

            return 0

        first = values[0]

        last = values[-1]

        return last - first

    @staticmethod
    def _trend_direction(slope):

        if slope > 0:

            return "UP"

        elif slope < 0:

            return "DOWN"

        return "FLAT"

    @staticmethod
    def _compression(distance20_50,
                     distance50_200):

        if (

            distance20_50 < 0.5

            and

            distance50_200 < 1

        ):

            return True

        return False

    @staticmethod
    def _expansion(

        old_distance,

        new_distance

    ):

        return new_distance > old_distance

    @staticmethod
    def analyze(

        latest: Dict,

        history: List[Dict]

    ):

        ema20 = []

        ema50 = []

        ema200 = []

        closes = []

        for row in history[-30:]:

            ema20.append(

                TrendEngine._safe(

                    row["ema20"]

                )

            )

            ema50.append(

                TrendEngine._safe(

                    row["ema50"]

                )

            )

            ema200.append(

                TrendEngine._safe(

                    row["ema200"]

                )

            )

            closes.append(

                TrendEngine._safe(

                    row["close"]

                )

            )

        current20 = ema20[-1]

        current50 = ema50[-1]

        current200 = ema200[-1]

        current_close = closes[-1]

        trend = "SIDEWAYS"

        trend_score = 0

        reasons = []

        if (

            current20 >

            current50 >

            current200

        ):

            trend = "STRONG_BULLISH"

            trend_score += 20

            reasons.append(

                "Perfect EMA Alignment"

            )

        elif (

            current20 >

            current50

        ):

            trend = "BULLISH"

            trend_score += 10

            reasons.append(

                "Bullish EMA Structure"

            )

        elif (

            current20 <

            current50 <

            current200

        ):

            trend = "STRONG_BEARISH"

            trend_score -= 20

            reasons.append(

                "Bearish EMA Structure"

            )

        slope20 = TrendEngine._slope(

            ema20[-10:]

        )

        slope50 = TrendEngine._slope(

            ema50[-10:]

        )

        slope200 = TrendEngine._slope(

            ema200[-10:]

        )

        direction20 = TrendEngine._trend_direction(

            slope20

        )

        direction50 = TrendEngine._trend_direction(

            slope50

        )

        direction200 = TrendEngine._trend_direction(

            slope200

        )

        if (

            direction20 == "UP"

            and

            direction50 == "UP"

        ):

            trend_score += 10

            reasons.append(

                "EMA Slopes Rising"

            )
          distance20_50 = TrendEngine._ema_distance(
            current20,
            current50
        )

        distance50_200 = TrendEngine._ema_distance(
            current50,
            current200
        )

        previous_distance = TrendEngine._ema_distance(
            ema20[-2],
            ema50[-2]
        )

        current_distance = distance20_50

        compression = TrendEngine._compression(
            distance20_50,
            distance50_200
        )

        expansion = TrendEngine._expansion(
            previous_distance,
            current_distance
        )

        if compression:

            trend_score += 3

            reasons.append(
                "EMA Compression"
            )

        if expansion:

            trend_score += 6

            reasons.append(
                "EMA Expansion"
            )

        trend_health = "WEAK"

        if (

            expansion

            and

            direction20 == "UP"

            and

            direction50 == "UP"

        ):

            trend_health = "HEALTHY"

            trend_score += 5

            reasons.append(
                "Trend Accelerating"
            )

        elif (

            compression

            and

            direction20 == "UP"

        ):

            trend_health = "BUILDING"

            reasons.append(
                "Trend Building"
            )

        pullback = "NONE"

        if (

            current_close >= current20 * 0.995

            and

            current_close <= current20 * 1.01

        ):

            pullback = "EMA20"

            trend_score += 5

            reasons.append(
                "Healthy EMA20 Pullback"

            )

        elif (

            current_close >= current50 * 0.995

            and

            current_close <= current50 * 1.01

        ):

            pullback = "EMA50"

            trend_score += 3

            reasons.append(

                "Deep EMA50 Pullback"

            )

        rejection = False

        latest_low = TrendEngine._safe(

            latest["low"]

        )

        latest_open = TrendEngine._safe(

            latest["open"]

        )

        if (

            latest_low < current20

            and

            current_close > current20

        ):

            rejection = True

            trend_score += 4

            reasons.append(

                "EMA20 Rejection"

            )

        elif (

            latest_low < current50

            and

            current_close > current50

        ):

            rejection = True

            trend_score += 3

            reasons.append(

                "EMA50 Rejection"

            )

        continuation_probability = 50

        if trend == "STRONG_BULLISH":

            continuation_probability += 20

        if expansion:

            continuation_probability += 10

        if rejection:

            continuation_probability += 8

        if pullback != "NONE":

            continuation_probability += 5

        continuation_probability = min(
            100,
            continuation_probability
        )
      trend_stage = "SIDEWAYS"

        if (
            trend == "STRONG_BULLISH"
            and expansion
            and direction20 == "UP"
        ):

            trend_stage = "MARKUP"

        elif (
            trend == "BULLISH"
            and compression
        ):

            trend_stage = "ACCUMULATION"

        elif (
            trend == "STRONG_BEARISH"
        ):

            trend_stage = "MARKDOWN"

        else:

            trend_stage = "DISTRIBUTION"

        overextended = False

        distance_from_ema20 = 0

        if current20 > 0:

            distance_from_ema20 = (

                abs(
                    current_close -
                    current20
                )

                /

                current20

            ) * 100

        if distance_from_ema20 >= 10:

            overextended = True

            trend_score -= 5

            reasons.append(

                "Price Too Far From EMA20"

            )

        trend_exhaustion = False

        if (

            overextended

            and

            not compression

            and

            direction20 == "UP"

        ):

            trend_exhaustion = True

            reasons.append(

                "Trend Exhaustion"

            )

        mean_reversion_risk = "LOW"

        if distance_from_ema20 >= 12:

            mean_reversion_risk = "HIGH"

        elif distance_from_ema20 >= 8:

            mean_reversion_risk = "MEDIUM"

        continuation_probability = max(

            0,

            min(

                100,

                continuation_probability

            )

        )

        reversal_probability = (

            100 -

            continuation_probability

        )

        if trend_exhaustion:

            reversal_probability += 15

            continuation_probability -= 15

        continuation_probability = max(
            0,
            min(
                100,
                continuation_probability
            )
        )

        reversal_probability = max(
            0,
            min(
                100,
                reversal_probability
            )
        )
trend_strength = "WEAK"

        if trend_score >= 35:

            trend_strength = "VERY STRONG"

        elif trend_score >= 25:

            trend_strength = "STRONG"

        elif trend_score >= 15:

            trend_strength = "MODERATE"

        trend_stability = "LOW"

        if (

            not compression

            and

            direction20 == direction50 == direction200

        ):

            trend_stability = "HIGH"

        elif direction20 == direction50:

            trend_stability = "MEDIUM"

        ai_confidence = 50

        ai_confidence += trend_score

        if expansion:

            ai_confidence += 5

        if rejection:

            ai_confidence += 4

        if pullback != "NONE":

            ai_confidence += 4

        if trend_exhaustion:

            ai_confidence -= 12

        ai_confidence = max(

            0,

            min(

                100,

                round(ai_confidence)

            )

        )

        trend_score = max(

            0,

            min(

                100,

                round(trend_score)

            )

        )

        reasons = list(

            dict.fromkeys(

                reasons

            )

        )

        return {

            "trend": trend,

            "trend_stage": trend_stage,

            "trend_strength": trend_strength,

            "trend_health": trend_health,

            "trend_stability": trend_stability,

            "trend_score": trend_score,

            "continuation_probability":

                continuation_probability,

            "reversal_probability":

                reversal_probability,

            "compression":

                compression,

            "expansion":

                expansion,

            "pullback":

                pullback,

            "rejection":

                rejection,

            "trend_exhaustion":

                trend_exhaustion,

            "mean_reversion_risk":

                mean_reversion_risk,

            "ema20_slope":

                round(slope20, 4),

            "ema50_slope":

                round(slope50, 4),

            "ema200_slope":

                round(slope200, 4),

            "ema20_50_distance":

                round(distance20_50, 2),

            "ema50_200_distance":

                round(distance50_200, 2),

            "distance_from_ema20":

                round(

                    distance_from_ema20,

                    2

                ),

            "confidence":

                ai_confidence,

            "reasons":

                reasons

}
