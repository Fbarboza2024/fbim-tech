import time
import docker
from datetime import datetime, timedelta
from governance.core.state_store import load_state
from governance.core.events import emit_event

# ================= CONFIG =================
CHECK_INTERVAL = 60            # segundos
KILL_SCORE = 40                # dispara
RECOVERY_SCORE = 65            # volta
COOLDOWN_MINUTES = 10          # tempo mínimo pausado

# Containers que NUNCA devem parar
PROTECTED = [
    "hr_governance",
    "strategist_governance",
    "scale_governance",
    "lab_governance",
    "audit_governance",
    "health_score_governance",
    "kill_switch_governance"
]

client = docker.from_env()

kill_active = False
kill_since = None

# ================= HELPERS =================
def get_health_score(events):
    scores = [
        e["payload"]["score"]
        for e in events
        if e["type"] == "COMPANY_HEALTH_SCORE"
    ]
    return scores[-1] if scores else 100

def stop_execution_containers():
    for c in client.containers.list():
        if c.name not in PROTECTED:
            try:
                c.stop()
            except:
                pass

def start_execution_containers():
    for c in client.containers.list(all=True):
        if c.name not in PROTECTED:
            try:
                c.start()
            except:
                pass

# ================= MAIN LOOP =================
while True:
    state = load_state()
    events = state.get("events", [])

    score = get_health_score(events)
    now = datetime.utcnow()

    # 🔴 DISPARAR KILL
    if score < KILL_SCORE and not kill_active:
        emit_event(
            "KILL_SWITCH_TRIGGERED",
            severity="critical",
            payload={"score": score}
        )
        stop_execution_containers()
        kill_active = True
        kill_since = now

    # 🟢 RECUPERAÇÃO AUTOMÁTICA
    if kill_active:
        elapsed = (now - kill_since).total_seconds() / 60

        if elapsed >= COOLDOWN_MINUTES and score >= RECOVERY_SCORE:
            emit_event(
                "SYSTEM_RECOVERED",
                payload={"score": score}
            )
            start_execution_containers()
            kill_active = False
            kill_since = None

    time.sleep(CHECK_INTERVAL)
