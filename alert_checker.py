from config import ALERT_THRESHOLD_PERCENT
from database import get_last_two_prices

# figures out if a stock moved enough to be worth an alert
# returns a message string if yes, or None if nothing interesting happened
def check_for_alert(ticker, current_price):
    history = get_last_two_prices(ticker)

    if len(history) < 2:
        # not enough data yet to compare, need at least 2 readings
        return None

    old_price = history[1]  # [0] is the one we just saved, [1] is the one before that
    percent_change = ((current_price - old_price) / old_price) * 100

    if abs(percent_change) >= ALERT_THRESHOLD_PERCENT:
        direction = "up" if percent_change > 0 else "down"
        msg = f"{ticker} is {direction} {abs(percent_change):.2f}% (${old_price:.2f} -> ${current_price:.2f})"
        return msg

    return None


def check_all(prices):
    alerts = []
    for ticker, price in prices.items():
        alert = check_for_alert(ticker, price)
        if alert:
            alerts.append(alert)
    return alerts