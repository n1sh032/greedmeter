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

# these are just reference lists now, actual watchlists live in the database per user
ALERT_COOLDOWN_HOURS = 4