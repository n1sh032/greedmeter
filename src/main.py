from price_fetcher import get_prices_for
from database import init_db, save_price, get_all_users, get_watchlist_for_user
from alert_checker import check_for_alert
from notifier import send_alert
from logger import log

def run():
    init_db()
    users = get_all_users()
    if not users:
        log("no users set up yet")
        return

    all_tickers = set()
    user_watchlists = {}
    for user_id, chat_id in users:
        wl = get_watchlist_for_user(user_id)
        user_watchlists[user_id] = wl
        for ticker, threshold in wl:
            all_tickers.add(ticker)

    prices = get_prices_for(list(all_tickers))
    log(f"checked prices, got {len(prices)} tickers across {len(users)} user(s)")

    for ticker, price in prices.items():
        save_price(ticker, price)

    for user_id, chat_id in users:
        for ticker, threshold in user_watchlists[user_id]:
            if ticker not in prices:
                continue
            alert = check_for_alert(user_id, ticker, threshold, prices[ticker])
            if alert:
                log(f"ALERT for user {user_id}: {alert}")
                send_alert(alert, chat_id)

    log("done")

if __name__ == "__main__":
    run()