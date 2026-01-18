import time
from governance.core.state_store import load_state
from governance.core.events import emit_event

INTERVAL = 3600

while True:
    state = load_state()
    for e in state["events"]:
        if e["type"] == "SCALE_CANDIDATE":
            emit_event("SCALE_UP_REQUEST", e["payload"])
    time.sleep(INTERVAL)
