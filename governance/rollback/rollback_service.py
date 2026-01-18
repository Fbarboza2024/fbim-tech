import time
import docker
from datetime import datetime, timedelta
from governance.core.state_store import load_state
from governance.core.events import emit_event

# ================= CONFIG =================
CHECK_INTERVAL = 120  # segundos
EVALUATION_WINDOW_MIN = 15  # tempo mínimo após deploy
ROLLBACK_SCORE_DROP = 15  # queda aceitável
STABLE_TAG = "stable"
CANDIDATE_TAG = "candidate"

client = docker.from_env()

# Guarda score anterior por container
last_scores = {}
deploy_times = {}

# ================= HELPERS =================
def get_health_score(events):
    scores = [
        e["payload"]["score"]
        for e in events
        if e["type"] == "COMPANY_HEALTH_SCORE"
    ]
    return scores[-1] if scores else None

def is_candidate(container):
    return CANDIDATE_TAG in container.image.tags[0]

def rollback(container):
    name = container.name
    image_base = container.image.tags[0].split(":")[0]

    emit_event(
        "ROLLBACK_TRIGGERED",
        severity="critical",
        payload={
            "container": name,
            "image": image_base
        }
    )

    try:
        container.stop()
        container.remove()
        client.containers.run(
            f"{image_base}:{STABLE_TAG}",
            name=name,
            detach=True,
            restart_policy={"Name": "always"},
            volumes=container.attrs["HostConfig"]["Binds"],
            environment=container.attrs["Config"]["Env"]
        )
    except Exception as e:
        emit_event(
            "ROLLBACK_FAILED",
            severity="critical",
            payload={"error": str(e)}
        )

# ================= MAIN LOOP =================
while True:
    state = load_state()
    events = state.get("events", [])
    score = get_health_score(events)

    if score is None:
        time.sleep(CHECK_INTERVAL)
        continue

    for c in client.containers.list():
        if not c.image.tags:
            continue

        tag = c.image.tags[0]

        if ":" not in tag:
            continue

        image, version = tag.split(":")

        # Só avalia candidates
        if version != CANDIDATE_TAG:
            continue

        now = datetime.utcnow()

        if c.name not in deploy_times:
            deploy_times[c.name] = now
            last_scores[c.name] = score
            continue

        elapsed = (now - deploy_times[c.name]).total_seconds() / 60

        if elapsed < EVALUATION_WINDOW_MIN:
            continue

        score_drop = last_scores[c.name] - score

        if score_drop >= ROLLBACK_SCORE_DROP:
            rollback(c)
            deploy_times.pop(c.name, None)
            last_scores.pop(c.name, None)
        else:
            # Promote to stable
            emit_event(
                "PROMOTE_TO_STABLE",
                payload={"container": c.name}
            )
            deploy_times.pop(c.name, None)
            last_scores.pop(c.name, None)

    time.sleep(CHECK_INTERVAL)
