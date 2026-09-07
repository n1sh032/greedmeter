from config import ALERT_THRESHOLDS, DEFAULT_THRESHOLD, ALERT_COOLDOWN_HOURS
from database import get_last_two_prices, get_last_alert_time, record_alert, init_alerts_table
from datetime import datetime, timezone, timedelta


def is_in_cooldown(ticker):
    last_alert = get_last_alert_time(ticker)
    if last_alert is None:
        return False  # never alerted before, so definitely not in cooldown

    last_alert_time = datetime.fromisoformat(last_alert)
    cutoff = datetime.now(timezone.utc) - timedelta(hours=ALERT_COOLDOWN_HOURS)
    return last_alert_time > cutoff


def check_for_alert(ticker, current_price):
    history = get_last_two_prices(ticker)

    if len(history) < 2:
        return None

    if is_in_cooldown(ticker):
        return None  # already alerted on this ticker recently, skip

    old_price = history[1]
    percent_change = ((current_price - old_price) / old_price) * 100

    threshold = ALERT_THRESHOLDS.get(ticker, DEFAULT_THRESHOLD)

    if abs(percent_change) >= threshold:
        direction = "up" if percent_change > 0 else "down"
        msg = f"{ticker} is {direction} {abs(percent_change):.2f}% (${old_price:.2f} -> ${current_price:.2f})"
        record_alert(ticker)  # mark that we alerted, starts the cooldown clock
        return msg

    return None


def check_all(prices):
    init_alerts_table()
    alerts = []
    for ticker, price in prices.items():
        alert = check_for_alert(ticker, price)
        if alert:
            alerts.append(alert)
    return alerts