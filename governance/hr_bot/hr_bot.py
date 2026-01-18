from datetime import datetime
from governance.core.state_store import load_state, save_state

TEST_DAYS = 60
OBS_DAYS = 7
QUAR_DAYS = 40
RETEST_DAYS = 15

def run_hr_cycle():
    state = load_state()
    now = datetime.utcnow()

    for bot_id, bot in state["bots"].items():
        since = datetime.fromisoformat(bot["since"])
        age = (now - since).days

        if bot["state"] == "TEST" and age >= TEST_DAYS:
            bot["state"] = "ACTIVE" if bot["ok"] else "OBSERVATION"
            bot["since"] = now.isoformat()

        elif bot["state"] == "OBSERVATION" and age >= OBS_DAYS:
            bot["state"] = "ACTIVE" if bot["ok"] else "QUARANTINE"
            bot["since"] = now.isoformat()

        elif bot["state"] == "QUARANTINE" and age >= QUAR_DAYS:
            bot["state"] = "RETEST"
            bot["since"] = now.isoformat()

        elif bot["state"] == "RETEST" and age >= RETEST_DAYS:
            bot["state"] = "ACTIVE" if bot["ok"] else "ARCHIVED"
            bot["since"] = now.isoformat()

    save_state(state)

if __name__ == "__main__":
    run_hr_cycle()
