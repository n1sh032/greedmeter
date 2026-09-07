# setup_user.py
# run this once to add yourself as a user with an initial watchlist
# you can re-run it later with different tickers to add more, or write a proper "edit watchlist" feature once the Flask app exists

from database import init_db, add_user, add_to_watchlist, get_all_users

# put your actual telegram chat id here (the one from earlier: 5969631036)
MY_CHAT_ID = "5969631036"

# ticker, threshold_percent pairs — same idea as before, just per-user now
MY_WATCHLIST = [
    ("AAPL", 2),
    ("MSFT", 2),
    ("TSLA", 4),
    ("NVDA", 4),
]

def setup():
    init_db()
    add_user(MY_CHAT_ID)

    # find the user_id that was just created (or already existed)
    users = get_all_users()
    user_id = None
    for uid, chat_id in users:
        if chat_id == MY_CHAT_ID:
            user_id = uid
            break

    for ticker, threshold in MY_WATCHLIST:
        add_to_watchlist(user_id, ticker, threshold)
        print(f"added {ticker} (threshold {threshold}%) to user {user_id}'s watchlist")

    print("done")


if __name__ == "__main__":
    setup()