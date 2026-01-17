from flask import Flask, redirect
from fbim.monetization.selector import select_offer

app = Flask(__name__)

@app.route("/r/<niche>")
def redirect_offer(niche):
    offer = select_offer(niche)
    return redirect(offer["url"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
