import os
import csv
import time
import requests
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
from threading import Thread
from dotenv import load_dotenv

# ================== ENV / PATHS ==================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

CSV_FILE = os.path.join(BASE_DIR, "trades.csv")
STATE_FILE = os.path.join(BASE_DIR, ".notified_orders")
IMG_FILE = os.path.join(BASE_DIR, "performance.png")

TG_MSG = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
TG_IMG = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

# ================== TELEGRAM ==================
def send_msg(text):
    requests.post(TG_MSG, json={"chat_id": CHAT_ID, "text": text}, timeout=10)

def send_img(path, caption):
    with open(path, "rb") as f:
        requests.post(
            TG_IMG,
            data={"chat_id": CHAT_ID, "caption": caption},
            files={"photo": f},
            timeout=20
        )

# ================== STATE ==================
def load_state():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE) as f:
        return set(line.strip() for line in f)

def save_state(order_id):
    with open(STATE_FILE, "a") as f:
        f.write(str(order_id) + "\n")

# ================== CSV ==================
def read_trades():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE) as f:
        return list(csv.DictReader(f))

# ================== NOTIFY ==================
def notify_trades():
    notified = load_state()

    while True:
        for r in read_trades():
            order_id = r.get("order_id")

            if not order_id or order_id in notified:
                continue

            if r["action"] == "OPEN" and r["status"] == "EXECUTED":
                send_msg(
                    "✅ ORDEM EXECUTADA\n"
                    f"Ativo: {r['symbol']}\n"
                    f"Direção: {r['side']}\n"
                    f"Qtd: {r['qty']}\n"
                    f"Order ID: {order_id}"
                )

            if r["action"] == "CLOSE" and r["status"] == "EXECUTED":
                pnl = float(r.get("pnl", 0))
                emoji = "🟢" if pnl >= 0 else "🔴"

                send_msg(
                    f"{emoji} ORDEM FECHADA\n"
                    f"Ativo: {r['symbol']}\n"
                    f"Direção: {r['side']}\n"
                    f"PnL: {pnl:.2f} USDT\n"
                    f"Order ID: {order_id}"
                )

            save_state(order_id)
            notified.add(order_id)

        time.sleep(3)

# ================== RELATÓRIOS ==================
def relatorio_periodo(dias, titulo):
    cutoff = date.today() - timedelta(days=dias)

    total = 0
    long_pnl = 0
    short_pnl = 0
    long_trades = 0
    short_trades = 0

    for r in read_trades():
        if r["action"] != "CLOSE":
            continue

        d = datetime.strptime(r["data"], "%Y-%m-%d %H:%M:%S").date()
        if d < cutoff:
            continue

        pnl = float(r.get("pnl", 0))
        total += pnl

        if r["side"] == "LONG":
            long_pnl += pnl
            long_trades += 1
        else:
            short_pnl += pnl
            short_trades += 1

    emoji = "🟢" if total >= 0 else "🔴"
  
    send_msg(
        f"📊 {titulo}\n\n"
        f"{emoji} Total: {total:.2f} USDT\n\n"
        f"🟢 LONG: {long_trades} | {long_pnl:.2f} USDT\n"
        f"🔴 SHORT: {short_trades} | {short_pnl:.2f} USDT"
    )

def daily_report():
    sent = False
    while True:
        now = datetime.now()
        if now.hour == 19 and not sent:
            relatorio_periodo(1, "RELATÓRIO DIÁRIO")
            sent = True
        if now.hour != 19:
            sent = False
        time.sleep(30)

# ================== GRÁFICO ==================
def grafico_periodo(dias, titulo):
    acc = 0
    series = []
    cutoff = date.today() - timedelta(days=dias)

    for r in read_trades():
        if r["action"] == "CLOSE":
            d = datetime.strptime(r["data"], "%Y-%m-%d %H:%M:%S").date()
            if d >= cutoff:
                acc += float(r.get("pnl", 0))
                series.append(acc)

    if not series:
        return

    plt.figure()
    plt.plot(series)
    plt.title(titulo)
    plt.xlabel("Trades")
    plt.ylabel("PnL Acumulado (USDT)")
    plt.grid()
    plt.savefig(IMG_FILE)
    plt.close()

    send_img(IMG_FILE, f"📈 {titulo}")

def weekly_monthly_graph():
    sw = sm = False
    while True:
        now = datetime.now()

        if now.weekday() == 0 and now.hour == 19 and not sw:
            grafico_periodo(7, "Performance Semanal")
            sw = True
        if now.weekday() != 0:
            sw = False

        if now.day == 1 and now.hour == 19 and not sm:
            grafico_periodo(30, "Performance Mensal")
            sm = True
        if now.day != 1:
            sm = False

        time.sleep(60)

# ================== START ==================
if __name__ == "__main__":
    print("📲 TELEGRAM NOTIFIER ONLINE — ORDER_ID MODE")

    Thread(target=notify_trades, daemon=True).start()
    Thread(target=daily_report, daemon=True).start()
    Thread(target=weekly_monthly_graph, daemon=True).start()

    while True:
        time.sleep(60)
