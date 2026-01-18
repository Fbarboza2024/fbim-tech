import time
import random
import docker
from datetime import datetime, timedelta
from governance.core.state_store import load_state
from governance.core.events import emit_event

# ================= CONFIG =================
CHAOS_INTERVAL_DAYS = 30          # uma vez por mês
COOLDOWN_HOURS = 24               # nunca roda em sequência
MAX_ACTIONS_PER_RUN = 1           # uma falha por rodada

# Containers protegidos (NUNCA tocar)
PROTECTED = [
    "hr_governance",
    "strategist_governance",
    "scale_governance",
    "lab_governance",
    "audit_governance",
    "health_score_governance",
    "kill_switch_governance",
    "rollback_governance",
    "chaos_governance"
]

client = docker.from_env()
last_run = None

# ================= CHAOS ACTIONS =================
def stop_random_container():
    containers = [
        c for c in client.containers.list()
        if c.name not in PROTECTED
    ]
    if not containers:
        return None

    target = random.choice(containers)
    target.stop()
    return f"Stopped container {target.name}"

def restart_random_container():
    containers = [
        c for c in client.containers.list(all=True)
        if c.name not in PROTECTED
    ]
    if not containers:
        return None

    target = random.choice(containers)
    target.restart()
    return f"Restarted container {target.name}"

CHAOS_ACTIONS = [
    stop_random_container,
    restart_random_container
]

# ================= MAIN LOOP =================
while True:
    now = datetime.utcnow()

    # cooldown
    if last_run and now - last_run < timedelta(hours=COOLDOWN_HOURS):
        time.sleep(3600)
        continue

    # roda apenas mensalmente
    if last_run and now - last_run < timedelta(days=CHAOS_INTERVAL_DAYS):
        time.sleep(3600)
        continue

    action = random.choice(CHAOS_ACTIONS)
    result = action()

    emit_event(
        "CHAOS_EXPERIMENT",
        severity="warning",
        payload={
            "action": action.__name__,
            "result": result,
            "time": now.isoformat()
        }
    )

    last_run = now
    time.sleep(3600)
