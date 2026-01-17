import random
import yaml
from fbim.lifecycle.stage import get_account_stage

TEMPLATES = yaml.safe_load(open("fbim/copy/templates.yaml"))

def generate_caption(account):
    stage = get_account_stage(account)
    key = "hard_cta" if stage == "hot" else "no_cta"
    return random.choice(TEMPLATES[key])
