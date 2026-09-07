from config import ALERT_COOLDOWN_HOURS
from database import get_last_two_prices, get_last_alert_time, record_alert
from datetime import datetime, timezone, timedelta


def is_in_cooldown(user_id, ticker):
    last_alert = get_last_alert_time(user_id, ticker)
    if last_alert is None:
        return False

    last_alert_time = datetime.fromisoformat(last_alert)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=ALERT_COOLDOWN_HOURS)
    return last_alert_time > cutoff


def check_for_alert(user_id, ticker, threshold_percent, current_price):
    history = get_last_two_prices(ticker)

    if len(history) < 2:
        return None

    if is_in_cooldown(user_id, ticker):
        return None

    old_price = history[1]
    percent_change = ((current_price - old_price) / old_price) * 100

    if abs(percent_change) >= threshold_percent:
        direction = "up" if percent_change > 0 else "down"
        msg = f"{ticker} is {direction} {abs(percent_change):.2f}% (${old_price:.2f} -> ${current_price:.2f})"
        record_alert(user_id, ticker)
        return msg

    return None