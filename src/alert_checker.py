from config import ALERT_COOLDOWN_HOURS
from database import get_last_two_prices, get_last_alert_time, record_alert
from datetime import datetime, timezone, timedelta

def is_in_cooldown(user_id, ticker):
    last = get_last_alert_time(user_id, ticker)
    if last is None:
        return False
    last_time = datetime.fromisoformat(last)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=ALERT_COOLDOWN_HOURS)
    return last_time > cutoff

def check_for_alert(user_id, ticker, threshold, current_price):
    history = get_last_two_prices(ticker)
    if len(history) < 2:
        return None
    if is_in_cooldown(user_id, ticker):
        return None

    old_price = history[1]
    change = ((current_price - old_price) / old_price) * 100

    if abs(change) >= threshold:
        direction = "up" if change > 0 else "down"
        msg = f"{ticker} is {direction} {abs(change):.2f}% (${old_price:.2f} -> ${current_price:.2f})"
        record_alert(user_id, ticker)
        return msg
    return None