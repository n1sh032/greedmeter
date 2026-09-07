import yfinance as yf
from config import WATCHLIST

# grabs the latest price for one ticker
# returns None if something goes wrong so one bad ticker doesnt crash the whole run
def get_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d", interval="1m")
        if data.empty:
            print(f"no data for {ticker}, skipping")
            return None
        return float(data["Close"].iloc[-1])
    except Exception as e:
        print(f"couldnt get {ticker}: {e}")
        return None


# loops through the whole watchlist and gets a price for each
def get_all_prices():
    prices = {}
    for ticker in WATCHLIST:
        price = get_price(ticker)
        if price is not None:
            prices[ticker] = price
    return prices


# lets me just run this file on its own to quickly check its working
if __name__ == "__main__":
    prices = get_all_prices()
    for ticker, price in prices.items():
        print(f"{ticker}: ${price:.2f}")