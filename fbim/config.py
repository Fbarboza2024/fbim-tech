import os
from dotenv import load_dotenv

load_dotenv()

def env(key, default=None, cast=str):
    v = os.getenv(key, default)
    return cast(v) if v is not None else None

MODE = env("MODE", "OBSERVATION")
LEVERAGE = env("LEVERAGE", 10, int)

WEBHOOK_TOKEN = env("WEBHOOK_TOKEN")

BINANCE_API_KEY = env("BINANCE_API_KEY")
BINANCE_API_SECRET = env("BINANCE_API_SECRET")

BYBIT_API_KEY = env("BYBIT_API_KEY")
BYBIT_API_SECRET = env("BYBIT_API_SECRET")

TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = env("TELEGRAM_CHAT_ID")

MAX_RISK_PER_TRADE = env("MAX_RISK_PER_TRADE", 0.01, float)
MAX_DRAWDOWN_DAILY = env("MAX_DRAWDOWN_DAILY", 0.02, float)
