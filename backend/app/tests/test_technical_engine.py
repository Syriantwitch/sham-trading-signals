from backend.app.services.strategy_engine.technical_engine import TechnicalEngine

def test_engine():
    # بيانات أسعار تجريبية للذهب (XAUUSD)
    mock_gold_prices = [2650, 2652, 2648, 2655, 2660, 2658, 2662, 2665, 2670]
    
    signal = TechnicalEngine.generate_signal("XAUUSD", mock_gold_prices)
    print("=== نتيجة تحليل محرك المؤشرات الفنية للذهب ===")
    print(signal)

if __name__ == "__main__":
    test_engine()