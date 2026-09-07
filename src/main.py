from price_fetcher import get_all_prices
from database import init_db, save_price
from alert_checker import check_all
from notifier import send_all_alerts
from logger import log

def run():
    init_db()

    prices = get_all_prices()
    log(f"checked prices, got {len(prices)} tickers")

    for ticker, price in prices.items():
        save_price(ticker, price)

    alerts = check_all(prices)

    if alerts:
        log(f"sending {len(alerts)} alert(s)")
        for alert in alerts:
            log(f"ALERT: {alert}")
        send_all_alerts(alerts)
    else:
        log("no alerts this time")


if __name__ == "__main__":
    run()