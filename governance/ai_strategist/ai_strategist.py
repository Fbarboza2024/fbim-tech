from governance.core.state_store import load_state
from governance.core.events import emit_event


def strategize():
state = load_state()


for bot, info in state.get("bots", {}).items():
if info.get("ok") and info.get("state") == "ACTIVE":
emit_event("SCALE_CANDIDATE", {"bot": bot})
