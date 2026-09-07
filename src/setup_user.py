# run once to add myself as a user with a starting watchlist
from database import init_db, add_user, add_to_watchlist, get_all_users

MY_CHAT_ID = "5969631036"

MY_WATCHLIST = [
    ("AAPL", 2),
    ("MSFT", 2),
    ("TSLA", 4),
    ("NVDA", 4),
]

def setup():
    init_db()
    add_user(MY_CHAT_ID)

    users = get_all_users()
    user_id = None
    for uid, chat_id in users:
        if chat_id == MY_CHAT_ID:
            user_id = uid
            break

    for ticker, threshold in MY_WATCHLIST:
        add_to_watchlist(user_id, ticker, threshold)
        print(f"added {ticker} ({threshold}%) to user {user_id}")

    print("done")

if __name__ == "__main__":
    setup()