import sys
import os
sys.path.insert(0, os.path.abspath(os.path.curdir))

from backend.app.services.strategy_engine.technical_engine import TechnicalEngine
from backend.app.services.distribution.telegram_bot import TelegramBotService

def test_bot_broadcast():
    print("=== اختبار توليد الإشارة وإرسالها عبر بوت التليجرام ===")
    mock_gold_prices = [2650, 2652, 2648, 2655, 2660, 2658, 2662, 2665, 2670]
    signal = TechnicalEngine.generate_signal("XAUUSD", mock_gold_prices)
    result = TelegramBotService.send_signal_to_channel(signal)
    
    print("\n[نتيجة صياغة البوت الإشارية]:")
    print(result.get("formatted_content", result))
    print("\n=== تمت عملية اختبار محرك المؤشرات والبوت بنجاح ===")

if __name__ == "__main__":
    test_bot_broadcast()
