from governance.core.events import emit_event

def report_pnl(bot_id: str, pnl: float):
    emit_event(
        event_type="PNL_REPORT",
        payload={
            "bot_id": bot_id,
            "pnl": pnl
        },
        severity="warning" if pnl < 0 else "info"
    )
