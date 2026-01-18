import time
from governance.core.state_store import load_state
from governance.core.events import emit_event

INTERVAL = 900  # 15 min

while True:
    state = load_state()

    for bot_id, bot in state["bots"].items():
        if bot["state"] == "ACTIVE" and bot["ok"]:
            emit_event("SCALE_CANDIDATE", {"bot_id": bot_id})

    time.sleep(INTERVAL)
