from governance.core.state_store import load_state, save_state

def update_bot_health(bot_id: str, score: float):
    """
    score > 0.6 → bot saudável
    """
    state = load_state()

    if bot_id not in state["bots"]:
        return

    state["bots"][bot_id]["ok"] = score > 0.6
    save_state(state)
