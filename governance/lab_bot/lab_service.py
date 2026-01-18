import time
from governance.core.registry import register_bot

INTERVAL = 86400  # 1 experimento / dia

i = 0
while True:
    name = f"lab_exp_{i}"
    register_bot(name, "experiment_content")
    i += 1
    time.sleep(INTERVAL)
