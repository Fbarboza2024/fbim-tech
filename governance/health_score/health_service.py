import time
from datetime import datetime, timedelta
from governance.core.state_store import load_state
from governance.core.events import emit_event

INTERVAL = 30 * 24 * 3600  # mensal

def calculate_score():
    state = load_state()
    bots = state.get("bots", {})
    events = state.get("events", [])
    now = datetime.utcnow()

    score = 0

    # 💰 Financeiro (30)
    monthly_pnl = sum(
        e["payload"].get("pnl", 0)
        for e in events
        if e["type"] == "PNL_REPORT"
    )
    if monthly_pnl > 0:
        score += 30

    # 🤖 Operacional (25)
    active = sum(1 for b in bots.values() if b["state"] == "ACTIVE")
    total = len(bots)
    if total > 0:
        ratio = active / total
        score += int(25 * ratio)

    # 🧠 Governança (20)
    recent_events = [
        e for e in events
        if datetime.fromisoformat(e["time"]) > now - timedelta(days=1)
    ]
    if recent_events:
        score += 20

    # 🌱 Crescimento (15)
    experiments = [
        b for b in bots.values()
        if b["type"].startswith("experiment")
    ]
    if experiments:
        score += 15

    # 👤 Dependência humana (10)
    human_events = [
        e for e in events
        if e["type"].startswith("HUMAN_")
    ]
    if len(human_events) == 0:
        score += 10

    return score

while True:
    score = calculate_score()
    emit_event(
        "COMPANY_HEALTH_SCORE",
        payload={"score": score}
    )
    time.sleep(INTERVAL)
