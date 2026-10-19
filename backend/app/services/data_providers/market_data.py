import requests

class MarketDataProvider:
    @staticmethod
    def get_recent_closes(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 25) -> list:
        # Map XAUUSD to PAXGUSDT (Gold-backed token on Binance) for live 24/7 spot gold tracking
        query_symbol = "PAXGUSDT" if symbol.upper() == "XAUUSD" else symbol.upper()
        url = f"https://api.binance.com/api/v3/klines?symbol={query_symbol}&interval={interval}&limit={limit}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [float(candle[4]) for candle in data]
        except Exception:
            pass
        # Fallback prices if offline
        if symbol.upper() == "XAUUSD":
            return [2650.0, 2652.5, 2648.0, 2655.0, 2660.0, 2658.5, 2662.0, 2665.0, 2671.5]
        return [67200.0, 67350.0, 67100.0, 67500.0, 67800.0, 67650.0, 67900.0, 68100.0, 68350.0]
