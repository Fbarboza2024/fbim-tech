import os
import csv
import ccxt
import logging
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# ================== ENV ==================
load_dotenv()

TOKEN_WEBHOOK = os.getenv("TOKEN_WEBHOOK")

BINANCE_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET = os.getenv("BINANCE_API_SECRET")

BYBIT_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET = os.getenv("BYBIT_API_SECRET")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TG_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# ================== CONFIG ==================
RISK_PERCENT = 0.05
LEVERAGE = 15

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "trades.csv")

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

# ================== TELEGRAM ==================
def tg(msg):
    requests.post(TG_URL, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=10)

# ================== BINANCE (INALTERADO) ==================
binance = ccxt.binance({
    "apiKey": BINANCE_KEY,
    "secret": BINANCE_SECRET,
    "options": {
        "defaultType": "future",
        "hedgeMode": True
    }
})

# ================== BYBIT FUTURES (NOVO) ==================
bybit = ccxt.bybit({
    "apiKey": BYBIT_KEY,
    "secret": BYBIT_SECRET,
    "options": {
        "defaultType": "swap",     # FUTUROS
        "defaultSettle": "USDT"    # USDT Perpetual
    }
})

# ================== CSV ==================
def salvar_trade(exchange, symbol, action, side, qty, entry, exit_price, pnl, order_id, status):
    exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow([
                "data","exchange","symbol","action",
                "side","qty","entrada","saida",
                "pnl","order_id","status"
            ])
        w.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            exchange, symbol, action, side,
            qty, entry, exit_price,
            pnl, order_id, status
        ])

# ================== UTILS ==================
def calc_size_binance(symbol, price):
    bal = binance.fetch_balance()
    usdt = bal["total"]["USDT"]
    size = (usdt * RISK_PERCENT * LEVERAGE) / price
    market = binance.market(symbol)
    size = max(size, market["limits"]["amount"]["min"])
    return float(binance.amount_to_precision(symbol, size))

def calc_size_bybit(symbol, price):
    bal = bybit.fetch_balance()
    usdt = bal["total"]["USDT"]
    size = (usdt * RISK_PERCENT * LEVERAGE) / price
    market = bybit.market(symbol)
    size = max(size, market["limits"]["amount"]["min"])
    return float(bybit.amount_to_precision(symbol, size))

# ================== BINANCE OPEN ==================
def abrir(symbol, side):
    price = binance.fetch_ticker(symbol)["last"]
    qty = calc_size_binance(symbol, price)
    pos_side = "LONG" if side == "buy" else "SHORT"
   order = binance.create_market_order(
        symbol=symbol,
        side=side,
        amount=qty,
        params={"positionSide": pos_side}
    )

    salvar_trade("BINANCE", symbol, "OPEN", pos_side, qty, price, "", 0, order["id"], "EXECUTED")
    tg(f"✅ BINANCE ABERTA {pos_side}\n{symbol}\nQtd: {qty}\nPreço: {price}")

# ================== BINANCE CLOSE ==================
def fechar(symbol):
    positions = binance.fetch_positions([symbol])

    for p in positions:
        qty = float(p.get("contracts", 0))
        if qty <= 0:
            continue

        is_long = p["side"] == "long"
        side = "sell" if is_long else "buy"
        pos_side = "LONG" if is_long else "SHORT"

        entry = float(p["entryPrice"])
        price = binance.fetch_ticker(symbol)["last"]

        pnl = (price - entry) * qty
        if not is_long:
            pnl *= -1

        order = binance.create_market_order(
            symbol=symbol,
            side=side,
            amount=qty,
            params={"positionSide": pos_side}
        )

        salvar_trade("BINANCE", symbol, "CLOSE", pos_side, qty, entry, price, round(pnl,2), order["id"], "EXECUTED")
        tg(f"🔒 BINANCE FECHADA {pos_side}\n{symbol}\nPnL: {pnl:.2f} USDT")

# ================== BYBIT OPEN (NOVO) ==================
def abrir_bybit(symbol, side):
    symbol_bb = symbol.replace("/", "")  # SOLUSDT
    price = bybit.fetch_ticker(symbol_bb)["last"]
    qty = calc_size_bybit(symbol_bb, price)

    pos_idx = 1 if side == "buy" else 2
    pos_side = "LONG" if side == "buy" else "SHORT"

    order = bybit.create_market_order(
        symbol=symbol_bb,
        side=side,
        amount=qty,
        params={"positionIdx": pos_idx}
    )

    salvar_trade("BYBIT", symbol_bb, "OPEN", pos_side, qty, price, "", 0, order["id"], "EXECUTED")
    tg(f"✅ BYBIT ABERTA {pos_side}\n{symbol_bb}\nQtd: {qty}\nPreço: {price}")

# ================== BYBIT CLOSE (NOVO) ==================
def fechar_bybit(symbol):
    symbol_bb = symbol.replace("/", "")
    positions = bybit.fetch_positions([symbol_bb])

    for p in positions:
        qty = float(p.get("contracts", 0))
        if qty <= 0:
            continue

        is_long = p["side"] == "long"
        side = "sell" if is_long else "buy"
        pos_idx = 1 if is_long else 2
        pos_side = "LONG" if is_long else "SHORT"

        entry = float(p["entryPrice"])
        price = bybit.fetch_ticker(symbol_bb)["last"]

        pnl = (price - entry) * qty
        if not is_long:
            pnl *= -1

        order = bybit.create_market_order(
            symbol=symbol_bb,
            side=side,
            amount=qty,
            params={"positionIdx": pos_idx}
        )

        salvar_trade("BYBIT", symbol_bb, "CLOSE", pos_side, qty, entry, price, round(pnl,2), order["id"], "EXECUTED")
        tg(f"🔒 BYBIT FECHADA {pos_side}\n{symbol_bb}\nPnL: {pnl:.2f} USDT")
      # ================== FLASK ==================
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    d = request.json
    if d.get("token") != TOKEN_WEBHOOK:
        return jsonify({"error":"token"}),403

    try:
        if d["side"] in ("buy","sell"):
            abrir(d["symbol"], d["side"])
            abrir_bybit(d["symbol"], d["side"])
            return jsonify({"status":"opened"})

        if d["side"] == "close":
            fechar(d["symbol"])
            fechar_bybit(d["symbol"])
            return jsonify({"status":"closed"})

    except Exception as e:
        logging.exception(e)
        return jsonify({"error":str(e)}),500

    return jsonify({"error":"invalid"}),400

# ================== START ==================
if __name__ == "__main__":
    logging.info("🚀 BOT FUTURES ONLINE — BINANCE + BYBIT (HEDGE)")
    app.run(host="0.0.0.0", port=5000)
