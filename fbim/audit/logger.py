import json, datetime, os
os.makedirs("logs", exist_ok=True)

def log_event(data):
    with open("logs/audit.log", "a") as f:
        f.write(json.dumps({
            "ts": datetime.datetime.utcnow().isoformat(),
            **data
        }) + "\n")  
