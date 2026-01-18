from governance.core.registry import register_bot

def create_experiment(exp_name: str, exp_type="content", meta=None):
    register_bot(
        bot_id=exp_name,
        bot_type=f"experiment_{exp_type}",
        meta=meta
    )

if __name__ == "__main__":
    create_experiment(
        "test_niche_fast",
        meta={"budget": "low", "duration_days": 7}
    )
