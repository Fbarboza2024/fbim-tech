from governance.core.state_store import load_state
from governance.core.events import emit_event

def run_strategy():
    state = load_state()

    for bot_id, bot in state["bots"].items():
        if bot["state"] == "ACTIVE" and bot["ok"]:
            emit_event(
                "SCALE_CANDIDATE",
                payload={"bot_id": bot_id}
            )

if __name__ == "__main__":
    run_strategy()
