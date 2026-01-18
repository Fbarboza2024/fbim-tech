from governance.core.events import emit_event


def report_pnl(bot_id, pnl):
if pnl < 0:
emit_event(
"NEGATIVE_PNL",
payload={"bot": bot_id, "pnl": pnl},
severity="warning"
)
