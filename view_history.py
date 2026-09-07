# view_history.py
import sqlite3
from datetime import datetime, timezone
from src.config import DB_FILE

def show_history():
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute(
        "SELECT ticker, price, checked_at FROM prices ORDER BY checked_at DESC"
    ).fetchall()
    conn.close()

    if not rows:
        print("no data yet, run main.py first")
        return

    print(f"{'TICKER':<8} {'PRICE':<12} {'WHEN':<25}")
    print("-" * 45)

    for ticker, price, checked_at in rows:
        # checked_at is stored in UTC, convert to local time for display
        utc_time = datetime.fromisoformat(checked_at)
        local_time = utc_time.astimezone()
        when = local_time.strftime("%d %b %Y, %I:%M %p")
        print(f"{ticker:<8} ${price:<11.2f} {when:<25}")


if __name__ == "__main__":
    show_history()