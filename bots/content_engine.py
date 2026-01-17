from fbim.copy.generator import generate_caption

def run():
    caption = generate_caption("tiktok_1")
    print("[CONTENT]", caption)

if __name__ == "__main__":
    run()
