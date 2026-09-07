import yfinance as yf

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


def get_prices_for(tickers):
    prices = {}
    for ticker in tickers:
        price = get_price(ticker)
        if price is not None:
            prices[ticker] = price
    return prices