import time
from datetime import datetime, timedelta
from governance.core.state_store import load_state
from governance.core.events import emit_event

INTERVAL = 30 * 24 * 3600  # 30 dias

def run_audit():
    state = load_state()
    bots = state.get("bots", {})
    events = state.get("events", [])

    now = datetime.utcnow()

    report = {
        "total_bots": len(bots),
        "active_bots": 0,
        "archived_bots": 0,
        "zombies": [],
        "inconsistent": [],
        "events_count": len(events),
    }

    for bot_id, bot in bots.items():
        if bot["state"] == "ACTIVE":
            report["active_bots"] += 1
        if bot["state"] == "ARCHIVED":
            report["archived_bots"] += 1

        # Zumbi: não muda estado há 90 dias
        since = datetime.fromisoformat(bot["since"])
        if (now - since).days > 90 and bot["state"] not in ["ARCHIVED"]:
            report["zombies"].append(bot_id)

        # Inconsistência
        if bot["ok"] and bot["state"] != "ACTIVE":
            report["inconsistent"].append(bot_id)

    emit_event(
        event_type="MONTHLY_AUDIT_REPORT",
        payload=report,
        severity="info"
    )

while True:
    run_audit()
    time.sleep(INTERVAL)
