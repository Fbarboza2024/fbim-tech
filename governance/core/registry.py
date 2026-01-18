from datetime import datetime
from .state_store import load_state, save_state

def register_bot(bot_id: str, bot_type: str, meta=None):
    state = load_state()

    if bot_id in state["bots"]:
        return  # evita sobrescrever

    state["bots"][bot_id] = {
        "type": bot_type,
        "state": "TEST",
        "since": datetime.utcnow().isoformat(),
        "ok": False,
        "meta": meta or {}
    }

    save_state(state)
