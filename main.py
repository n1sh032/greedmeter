from price_fetcher import get_all_prices
from database import init_db, save_price
from alert_checker import check_all
from notifier import send_all_alerts


def run():
    init_db()  # makes sure the table exists before we try to use it

    prices = get_all_prices()
    print(f"got prices for {len(prices)} tickers")

    for ticker, price in prices.items():
        save_price(ticker, price)

    alerts = check_all(prices)

    if alerts:
        print(f"sending {len(alerts)} alert(s)")
        send_all_alerts(alerts)
    else:
        print("no alerts this time")


if __name__ == "__main__":
    run()