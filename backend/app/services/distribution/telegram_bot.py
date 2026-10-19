import requests
from backend.app.db.database import get_settings

class TelegramBotService:
    @staticmethod
    def format_signal_message(signal_data: dict) -> str:
        symbol = signal_data.get("symbol", "UNKNOWN")
        recommendation = signal_data.get("recommendation", "HOLD")
        confidence = signal_data.get("confidence_score", "85%")
        entry = signal_data.get("entry_price", 0)
        sl = signal_data.get("stop_loss", 0)
        tp1 = signal_data.get("take_profit_1", 0)
        tp2 = signal_data.get("take_profit_2", 0)
        rsi = signal_data.get("rsi_indicator", 0)
        macd = signal_data.get("macd_trend", "ACTIVE")

        emoji = "🟢" if "BUY" in recommendation else "🔴"

        return (
            f"{emoji} *SHAM DIGITAL SOLUTIONS — إشارة تداول ذكية* {emoji}\n\n"
            f"📊 *الأصل المالي:* `{symbol}`\n"
            f"📈 *نوع الصفقة:* `{recommendation}`\n"
            f"🔥 *قوة الإشارة:* `{confidence}` | *MACD:* `{macd}`\n"
            f"💵 *سعر الدخول:* `${entry}`\n\n"
            f"🎯 *الأهداف:* \n"
            f"  • الهدف الأول (TP1): `${tp1}`\n"
            f"  • الهدف الثاني (TP2): `${tp2}`\n\n"
            f"🛑 *وقف الخسارة (SL):* `${sl}`\n"
            f"📉 *مؤشر RSI:* `{rsi}`\n\n"
            f"⚡ _إدارة رأس المال أساس النجاح — لا تخاطر بأكثر من 2%_"
        )

    @classmethod
    def send_signal_to_channel(cls, signal_data: dict) -> dict:
        cfg = get_settings()
        token = cfg.get("telegram_bot_token", "MOCK_BOT_TOKEN")
        channel_id = cfg.get("telegram_channel_id", "@ShamSignalsVIP")
        message_text = cls.format_signal_message(signal_data)
        
        if token == "MOCK_BOT_TOKEN" or not token.strip():
            return {
                "status": "SUCCESS",
                "mode": "MOCK",
                "message": "وضع المحاكاة (أدخل توكن البوت الحقيقي في إعدادات الإدارة للإرسال الفعلي لتليجرام)",
                "formatted_content": message_text
            }

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": channel_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            res_json = response.json()
            return {
                "status": "SENT_TO_TELEGRAM" if res_json.get("ok") else "TELEGRAM_API_ERROR",
                "telegram_response": res_json,
                "formatted_content": message_text
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e), "formatted_content": message_text}
