from datetime import datetime
from .state_store import load_state, save_state

MAX_EVENTS = 1000

def emit_event(event_type: str, payload=None, severity="info"):
    state = load_state()

    state["events"].append({
        "time": datetime.utcnow().isoformat(),
        "type": event_type,
        "severity": severity,
        "payload": payload or {}
    })

    # Limitar tamanho (CRÍTICO)
    state["events"] = state["events"][-MAX_EVENTS:]

    save_state(state)
