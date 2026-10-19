class RiskCalculator:
    @staticmethod
    def calculate_position_size(account_balance: float, risk_percentage: float, entry_price: float, stop_loss_price: float, asset_type: str = "CRYPTO"):
        if account_balance <= 0 or risk_percentage <= 0:
            return {"error": "Invalid balance or risk."}
        risk_amount = account_balance * (risk_percentage / 100.0)
        price_distance = abs(entry_price - stop_loss_price)
        if price_distance == 0:
            return {"error": "Entry and Stop Loss cannot match."}
        if asset_type.upper() == "GOLD":
            lot_size = round(risk_amount / (price_distance * 100), 2)
            return {"risk_usd": round(risk_amount, 2), "lot_size": max(0.01, lot_size), "asset": "Gold"}
        else:
            units = round(risk_amount / price_distance, 4)
            return {"risk_usd": round(risk_amount, 2), "units": units, "asset": "Crypto"}
