import json
from pathlib import Path
from filelock import FileLock

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

STATE_FILE = DATA_DIR / "global_state.json"
LOCK_FILE = FileLock(str(STATE_FILE) + ".lock")

if not STATE_FILE.exists():
    STATE_FILE.write_text(json.dumps({
        "bots": {},
        "events": []
    }, indent=2))

def load_state():
    with LOCK_FILE:
        return json.loads(STATE_FILE.read_text())

def save_state(state: dict):
    with LOCK_FILE:
        STATE_FILE.write_text(json.dumps(state, indent=2))
