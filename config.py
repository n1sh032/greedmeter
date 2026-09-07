#config for the watchlist and stuff

#us tech stocks
us_tech = ["AAPL", "MSFT", "TSLA", "NVDA"]
#other us stocks i wanted to add
us_other = ["JPM", "KO", "DIS"]
#singapore stocks (DBS, OCBC, Singtel)
sg_stocks = ["D05.SI", "O39.SI", "Z74.SI"]

markets = {
    "us_tech": us_tech,
    "us_other": us_other,
    "sg": sg_stocks
}

# change this depending on what market you wanna check
active_market = "us_tech"
WATCHLIST = markets[active_market]

ALERT_THRESHOLD_PERCENT = 0.01  # % move that counts as worth an alert

DB_FILE = "prices.db"
CHECK_INTERVAL_MINUTES = 15