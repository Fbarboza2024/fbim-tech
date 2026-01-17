import yaml

OFFERS = yaml.safe_load(open("fbim/monetization/offers.yaml"))["offers"]

def select_offer(niche):
    for o in OFFERS:
        if o["niche"] == niche:
            return o
