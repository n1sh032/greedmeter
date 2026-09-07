from flask import Flask, render_template, request, redirect
from database import init_db, get_watchlist_for_user, add_to_watchlist, get_last_two_prices
import csv
import os
from price_fetcher import get_price
from database import save_price
from database import init_db, get_watchlist_for_user, add_to_watchlist, get_last_two_prices, remove_from_watchlist

app = Flask(__name__)

MY_USER_ID = 1  # hardcoded for now, single user

TICKERS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tickers.csv")


def load_tickers():
    tickers = []
    with open(TICKERS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tickers.append(row)
    return tickers


ALL_TICKERS = load_tickers()  # load once when the app starts, not on every search


@app.route("/")
def dashboard():
    watchlist = get_watchlist_for_user(MY_USER_ID)

    rows = []
    for ticker, threshold in watchlist:
        prices = get_last_two_prices(ticker)
        latest_price = prices[0] if prices else None
        rows.append({
            "ticker": ticker,
            "threshold": threshold,
            "price": latest_price
        })

    return render_template("dashboard.html", rows=rows)



@app.route("/add", methods=["POST"])
def add_ticker():
    ticker = request.form.get("ticker").upper().strip()
    threshold = float(request.form.get("threshold"))
    add_to_watchlist(MY_USER_ID, ticker, threshold)

    # fetch a price right away so it doesn't sit empty until the next scheduled run
    price = get_price(ticker)
    if price is not None:
        save_price(ticker, price)

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
@app.route("/delete", methods=["POST"])
def delete_ticker():
    ticker = request.form.get("ticker")
    remove_from_watchlist(MY_USER_ID, ticker)
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)