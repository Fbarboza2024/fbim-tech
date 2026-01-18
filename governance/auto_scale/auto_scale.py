from governance.core.events import emit_event


def scale(bot_id):
emit_event("SCALE_UP", {"bot": bot_id})
