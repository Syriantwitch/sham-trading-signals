import math

class TechnicalEngine:
    @staticmethod
    def calculate_sma(prices: list, period: int = 14) -> float:
        if len(prices) < period:
            return sum(prices) / len(prices) if prices else 0.0
        return sum(prices[-period:]) / period

    @staticmethod
    def calculate_ema(prices: list, period: int) -> float:
        if not prices:
            return 0.0
        k = 2 / (period + 1)
        ema = prices[0]
        for price in prices[1:]:
            ema = (price * k) + (ema * (1 - k))
        return ema

    @classmethod
    def calculate_macd(cls, prices: list) -> dict:
        ema12 = cls.calculate_ema(prices[-26:], 12)
        ema26 = cls.calculate_ema(prices[-26:], 26)
        macd_line = ema12 - ema26
        trend = "BULLISH" if macd_line > 0 else "BEARISH"
        return {"macd": round(macd_line, 2), "trend": trend}

    @classmethod
    def calculate_bollinger(cls, prices: list, period: int = 20) -> dict:
        subset = prices[-period:] if len(prices) >= period else prices
        sma = sum(subset) / len(subset)
        variance = sum((x - sma) ** 2 for x in subset) / len(subset)
        std_dev = math.sqrt(variance)
        return {
            "upper": round(sma + (2 * std_dev), 2),
            "middle": round(sma, 2),
            "lower": round(sma - (2 * std_dev), 2)
        }

    @staticmethod
    def calculate_rsi(prices: list, period: int = 14) -> float:
        if len(prices) < period + 1:
            return 50.0
        gains, losses = 0.0, 0.0
        for i in range(1, period + 1):
            change = prices[-i] - prices[-i-1]
            if change > 0:
                gains += change
            else:
                losses -= change
        avg_gain = gains / period
        avg_loss = losses / period if losses != 0 else 0.001
        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 2)

    @classmethod
    def generate_signal(cls, symbol: str, recent_prices: list) -> dict:
        if not recent_prices or len(recent_prices) < 5:
            return {"error": "Insufficient price data"}

        current_price = recent_prices[-1]
        rsi = cls.calculate_rsi(recent_prices)
        sma = cls.calculate_sma(recent_prices)
        macd_data = cls.calculate_macd(recent_prices)
        bb = cls.calculate_bollinger(recent_prices)

        # Multi-Indicator Scoring
        bullish_score = 0
        if current_price > sma: bullish_score += 25
        if macd_data["macd"] > 0: bullish_score += 25
        if rsi < 35: bullish_score += 30
        elif 45 <= rsi <= 65: bullish_score += 20
        if current_price <= bb["lower"] * 1.01: bullish_score += 20

        if bullish_score >= 50:
            action = "BUY (اتجاه صاعد)"
            confidence = min(95, 55 + bullish_score // 2)
        else:
            action = "SELL (اتجاه هابط)"
            confidence = min(95, 95 - bullish_score // 2)

        is_gold = "XAU" in symbol.upper()
        spread_factor = 0.005 if is_gold else 0.02

        stop_loss = round(current_price * (1 - spread_factor), 2) if "BUY" in action else round(current_price * (1 + spread_factor), 2)
        tp1 = round(current_price * (1 + spread_factor * 1.5), 2) if "BUY" in action else round(current_price * (1 - spread_factor * 1.5), 2)
        tp2 = round(current_price * (1 + spread_factor * 3.0), 2) if "BUY" in action else round(current_price * (1 - spread_factor * 3.0), 2)

        return {
            "symbol": symbol.upper(),
            "current_price": current_price,
            "rsi_indicator": rsi,
            "sma_indicator": round(sma, 2),
            "macd_trend": macd_data["trend"],
            "bb_upper": bb["upper"],
            "bb_lower": bb["lower"],
            "recommendation": action,
            "confidence_score": f"{confidence}%",
            "entry_price": current_price,
            "stop_loss": stop_loss,
            "take_profit_1": tp1,
            "take_profit_2": tp2
        }
