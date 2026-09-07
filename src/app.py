from flask import Flask, render_template, request, redirect
from database import (
    init_db, get_watchlist_for_user, add_to_watchlist,
    get_last_two_prices, remove_from_watchlist, save_price
)
from price_fetcher import get_price
import csv
import os

app = Flask(__name__)
MY_USER_ID = 1  # just me for now

TICKERS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tickers.csv")

def load_tickers():
    tickers = []
    with open(TICKERS_FILE, newline="") as f:
        for row in csv.DictReader(f):
            tickers.append(row)
    return tickers

ALL_TICKERS = load_tickers()

@app.route("/")
def dashboard():
    watchlist = get_watchlist_for_user(MY_USER_ID)
    rows = []
    for ticker, threshold in watchlist:
        prices = get_last_two_prices(ticker)
        latest = prices[0] if prices else None

        change = None
        if len(prices) == 2 and prices[1] != 0:
            change = ((prices[0] - prices[1]) / prices[1]) * 100

        rows.append({"ticker": ticker, "threshold": threshold, "price": latest, "change": change})

    return render_template("dashboard.html", rows=rows)

@app.route("/add", methods=["POST"])
def add_ticker():
    ticker = request.form.get("ticker").upper().strip()
    threshold = float(request.form.get("threshold"))
    add_to_watchlist(MY_USER_ID, ticker, threshold)

    price = get_price(ticker)
    if price is not None:
        save_price(ticker, price)

    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete_ticker():
    ticker = request.form.get("ticker")
    remove_from_watchlist(MY_USER_ID, ticker)
    return redirect("/")

@app.route("/search_tickers")
def search_tickers():
    query = request.args.get("q", "").upper()
    if len(query) < 1:
        return {"results": []}

    matches = []
    for t in ALL_TICKERS:
        if query in t["symbol"].upper() or query in t["name"].upper():
            matches.append(t)
        if len(matches) >= 10:
            break

    return {"results": matches}

if __name__ == "__main__":
    init_db()
    app.run(debug=True)