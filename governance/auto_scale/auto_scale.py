from governance.core.events import emit_event

def scale_up(bot_id: str):
    emit_event(
        "SCALE_UP_REQUEST",
        payload={"bot_id": bot_id}
    )

if __name__ == "__main__":
    pass
