import json
from pathlib import Path


DATA = Path("data")
DATA.mkdir(exist_ok=True)
STATE_FILE = DATA / "global_state.json"


if not STATE_FILE.exists():
STATE_FILE.write_text("{}")


def load_state():
return json.loads(STATE_FILE.read_text())


def save_state(state: dict):
STATE_FILE.write_text(json.dumps(state, indent=2))
