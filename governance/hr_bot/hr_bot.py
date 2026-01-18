from datetime import datetime, timedelta
from governance.core.state_store import load_state, save_state


TEST_DAYS = 60
OBS_DAYS = 7
QUAR_DAYS = 40
RETEST_DAYS = 15


def run_hr_cycle():
state = load_state()
now = datetime.utcnow()


for bot, info in state.get("bots", {}).items():
since = datetime.fromisoformat(info["since"])
age = (now - since).days


if info["state"] == "TEST" and age >= TEST_DAYS:
info["state"] = "ACTIVE" if info["ok"] else "OBSERVATION"
info["since"] = now.isoformat()


elif info["state"] == "OBSERVATION" and age >= OBS_DAYS:
info["state"] = "ACTIVE" if info["ok"] else "QUARANTINE"
info["since"] = now.isoformat()


elif info["state"] == "QUARANTINE" and age >= QUAR_DAYS:
info["state"] = "RETEST"
info["since"] = now.isoformat()


elif info["state"] == "RETEST" and age >= RETEST_DAYS:
info["state"] = "ACTIVE" if info["ok"] else "ARCHIVED"
info["since"] = now.isoformat()


save_state(state)
