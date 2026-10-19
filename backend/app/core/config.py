import os

class Config:
    PROJECT_NAME: str = "Smart Trading Signals Platform"
    ENV: str = os.getenv("ENV", "development")
    BINANCE_BASE_URL: str = "https://api.binance.com"
    
    # Telegram Configuration
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "MOCK_BOT_TOKEN")
    TELEGRAM_CHANNEL_ID: str = os.getenv("TELEGRAM_CHANNEL_ID", "@mock_signals_channel")

    # ShamCash Configuration (Manual Verification)
    SHAMCASH_ACCOUNT_NUMBER: str = os.getenv("SHAMCASH_ACCOUNT_NUMBER", "09XXXXXXXX")
    SHAMCASH_ACCOUNT_NAME: str = "SHAM DIGITAL SOLUTIONS"
