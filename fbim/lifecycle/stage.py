from fbim.feedback.collector import collect_metrics

def get_account_stage(account):
    m = collect_metrics(account)

    if m["age_days"] >= 14 and m["avg_views"] >= 2000:
        return "hot"

    if m["age_days"] >= 7:
        return "warm"

    return "cold"
