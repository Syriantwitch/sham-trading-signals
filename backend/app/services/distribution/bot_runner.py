import sys
import os
import time
import requests

sys.path.insert(0, os.path.abspath(os.path.curdir))

from backend.app.db.database import get_settings
from backend.app.services.data_providers.market_data import MarketDataProvider
from backend.app.services.strategy_engine.technical_engine import TechnicalEngine

# تخزين لغة كل مستخدم مؤقتاً (افتراضياً: عربي)
user_languages = {}

def run_pro_bot():
    print("=== SHAM DIGITAL SOLUTIONS - Pro Telegram Bot Running ===")
    processed = set()
    
    while True:
        try:
            cfg = get_settings()
            token = cfg.get("telegram_bot_token", "MOCK_BOT_TOKEN")
            shamcash = cfg.get("shamcash_number", "09XXXXXXXX")

            if token == "MOCK_BOT_TOKEN" or not token.strip():
                print("Bot is in MOCK mode. Please update your Bot Token in the Web Admin Panel.")
                time.sleep(10)
                continue

            url = f"https://api.telegram.org/bot{token}/getUpdates?offset=-1"
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                if data.get("ok") and data.get("result"):
                    for u in data["result"]:
                        uid = u["update_id"]
                        if uid in processed: continue
                        processed.add(uid)

                        # معالجة الضغط على الأزرار (Callback Queries)
                        if "callback_query" in u:
                            cq = u["callback_query"]
                            chat_id = cq["message"]["chat"]["id"]
                            data_val = cq["data"]
                            
                            if data_val == "lang_ar":
                                user_languages[chat_id] = "ar"
                                send_welcome(token, chat_id, "ar", shamcash)
                            elif data_val == "lang_en":
                                user_languages[chat_id] = "en"
                                send_welcome(token, chat_id, "en", shamcash)
                            elif data_val == "btn_signals":
                                lang = user_languages.get(chat_id, "ar")
                                send_signals(token, chat_id, lang)
                            elif data_val == "btn_plans":
                                lang = user_languages.get(chat_id, "ar")
                                send_plans(token, chat_id, lang, shamcash)
                            elif data_val == "btn_shamcash":
                                lang = user_languages.get(chat_id, "ar")
                                send_shamcash(token, chat_id, lang, shamcash)
                            continue

                        # معالجة الرسائل النصية والأوامر
                        msg = u.get("message")
                        if msg and "text" in msg:
                            chat_id = msg["chat"]["id"]
                            txt = msg["text"].strip()
                            lang = user_languages.get(chat_id, "ar")

                            if txt == "/start":
                                ask_language(token, chat_id)
                            elif txt == "/signals":
                                send_signals(token, chat_id, lang)
                            elif txt == "/plans":
                                send_plans(token, chat_id, lang, shamcash)
                            elif txt == "/shamcash":
                                send_shamcash(token, chat_id, lang, shamcash)
                            else:
                                reply = "أهلاً بك! يرجى استخدام القائمة أدناه أو الأوامر المتاحة." if lang == "ar" else "Welcome! Please use the menu below or available commands."
                                requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": reply})
        except Exception as e:
            print("Error:", e)
        time.sleep(2)

def ask_language(token, chat_id):
    text = (
        "🌟 **أهلاً بك في منصة SHAM DIGITAL SOLUTIONS** 🌟\n\n"
        "يرجى اختيار لغة العرض المفضلة لديك:\n"
        "Please choose your preferred language:"
    )
    keyboard = {
        "inline_keyboard": [
            [{"text": "🇸🇦 العربية", "callback_data": "lang_ar"}, {"text": "🇬🇧 English", "callback_data": "lang_en"}]
        ]
    }
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown", "reply_markup": keyboard})

def send_welcome(token, chat_id, lang, shamcash):
    if lang == "ar":
        text = (
            "✨ **مرحباً بك في عالم التداول الاحترافي!** ✨\n\n"
            "نحن سعداء انضمامك إلينا. يسعدنا تقديم أحدث إشارات الذهب والعملات الرقمية المبنية على تحليل فني دقيق.\n\n"
            "👇 **اختر ما تحب استكشافه من القائمة أدناه:**"
        )
    else:
        text = (
            "✨ **Welcome to Professional Trading!** ✨\n\n"
            "We are thrilled to have you. Enjoy our premium Gold and Crypto signals powered by advanced technical analysis.\n\n"
            "👇 **Explore our features below:**"
        )
    
    btn_sig = "📊 الإشارات الحية" if lang == "ar" else "📊 Live Signals"
    btn_pln = "👑 باقات VIP" if lang == "ar" else "👑 VIP Plans"
    btn_shm = "💳 حساب شام كاش" if lang == "ar" else "💳 ShamCash Info"

    keyboard = {
        "inline_keyboard": [
            [{"text": btn_sig, "callback_data": "btn_signals"}],
            [{"text": btn_pln, "callback_data": "btn_plans"}, {"text": btn_shm, "callback_data": "btn_shamcash"}]
        ]
    }
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown", "reply_markup": keyboard})

def send_signals(token, chat_id, lang):
    prices = MarketDataProvider.get_recent_closes("XAUUSD")
    sig = TechnicalEngine.generate_signal("XAUUSD", prices)
    
    if lang == "ar":
        text = (
            f"🟢 **أحدث توصية ذهب حية (XAUUSD)**\n\n"
            f"📈 **الاتجاه:** `{sig['recommendation']}`\n"
            f"💵 **سعر الدخول:** `${sig['entry_price']}`\n"
            f"🎯 **الهدف الأول (TP1):** `${sig['take_profit_1']}`\n"
            f"🛑 **وقف الخسارة (SL):** `${sig['stop_loss']}`\n\n"
            f"⚡ *تمنياتنا لك بالتوفيق الدائم!*"
        )
    else:
        text = (
            f"🟢 **Latest Gold Live Signal (XAUUSD)**\n\n"
            f"📈 **Action:** `{sig['recommendation']}`\n"
            f"💵 **Entry Price:** `${sig['entry_price']}`\n"
            f"🎯 **Take Profit 1:** `${sig['take_profit_1']}`\n"
            f"🛑 **Stop Loss:** `${sig['stop_loss']}`\n\n"
            f"⚡ *Trade with proper risk management!*"
        )
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

def send_plans(token, chat_id, lang, shamcash):
    if lang == "ar":
        text = (
            "👑 **باقات الاشتراك الفاخرة (VIP)**\n\n"
            "1️⃣ **الباقة الشهرية:** `$30`\n"
            "2️⃣ **الباقة الربع سنوية:** `$75` (توفير ممتاز)\n\n"
            f"💳 **طريقة الاشتراك:** قم بتحويل المبلغ عبر تطبيق شام كاش إلى الرقم المعتمد: `{shamcash}`، ثم أرسل رقم العملية (TX ID) عبر موقعنا لتفعيل حسابك فوراً بكل سهولة."
        )
    else:
        text = (
            "👑 **VIP Subscription Plans**\n\n"
            "1️⃣ **Monthly Plan:** `$30`\n"
            "2️⃣ **Quarterly Plan:** `$75` (Best Value)\n\n"
            f"💳 **How to Subscribe:** Transfer the amount via ShamCash to our official account: `{shamcash}`, then submit your Transaction ID on our web portal for instant activation."
        )
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

def send_shamcash(token, chat_id, lang, shamcash):
    if lang == "ar":
        text = f"💳 **حساب شام كاش الرسمي لشركة SHAM DIGITAL SOLUTIONS:**\n\n`{shamcash}`\n\n*يرجى الاحتفاظ برقم العملية (TX ID) بعد التحويل لتأكيد الاشتراك.*"
    else:
        text = f"💳 **Official ShamCash Account for SHAM DIGITAL SOLUTIONS:**\n\n`{shamcash}`\n\n*Please keep your Transaction ID after transferring to verify your subscription.*"
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"})

if __name__ == "__main__":
    run_pro_bot()
