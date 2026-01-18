from datetime import datetime
from .state_store import load_state, save_state


def emit_event(event_type, payload=None, severity="info"):
state = load_state()
state.setdefault("events", []).append({
"time": datetime.utcnow().isoformat(),
"type": event_type,
"severity": severity,
"payload": payload or {}
})
save_state(state)
