from .state_store import load_state, save_state
from datetime import datetime


def register_bot(bot_id, bot_type):
state = load_state()
state.setdefault("bots", {})[bot_id] = {
"type": bot_type,
"state": "TEST",
"since": datetime.utcnow().isoformat(),
"ok": False
}
save_state(state)
