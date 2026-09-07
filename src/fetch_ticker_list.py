# fetch_ticker_list.py
import requests
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "tickers.csv")

URL = "https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt"


def fetch_tickers():
    response = requests.get(URL)
    lines = response.text.splitlines()

    data_lines = lines[1:-1]

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["symbol", "name"])

        for line in data_lines:
            parts = line.split("|")
            symbol = parts[0]
            name = parts[1]
            writer.writerow([symbol, name])

    print(f"saved {len(data_lines)} tickers to {OUTPUT_FILE}")


if __name__ == "__main__":
    fetch_tickers()