#config for the watchlist and stuff

#us tech stocks
us_tech = ["AAPL", "MSFT", "TSLA", "NVDA"]
#other us stocks i wanted to add
us_other = ["JPM", "KO", "DIS"]
#singapore stocks (DBS, OCBC, Singtel) - need the .SI at the end for yfinance to find them
sg_stocks = ["D05.SI", "O39.SI", "Z74.SI"]

markets = {
    "us_tech": us_tech,
    "us_other": us_other,
    "sg": sg_stocks
}

# change this depending on what market you wanna check
active_market = "us_tech"
WATCHLIST = markets[active_market]

# per-ticker alert thresholds (% move that counts as worth an alert)
# stable/blue-chip stocks get a lower threshold, volatile ones get a higher one
ALERT_THRESHOLDS = {
    "AAPL": 2,
    "MSFT": 2,
    "TSLA": 4,
    "NVDA": 4,
    "JPM": 2,
    "KO": 1,
    "DIS": 2,
}

DEFAULT_THRESHOLD = 2  # fallback for any ticker not in the dict above
ALERT_COOLDOWN_HOURS = 4

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "data", "prices.db")
CHECK_INTERVAL_MINUTES = 15