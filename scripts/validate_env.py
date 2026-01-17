import os, sys

REQUIRED = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "BINANCE_API_KEY",
    "BINANCE_API_SECRET",
    "WEBHOOK_TOKEN"
]

missing = [k for k in REQUIRED if not os.getenv(k)]

if missing:
    print("❌ Variáveis faltando:", missing)
    sys.exit(1)

print("✅ .env válido")
