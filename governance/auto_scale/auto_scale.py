from governance.core.events import emit_event

def scale_up(bot_id: str):
    emit_event(
        event_type="SCALE_UP",
        payload={"bot_id": bot_id}
    )
