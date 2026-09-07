# grabs the list of nasdaq tickers so the search bar has something to search through
import requests
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "tickers.csv")
URL = "https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt"

def fetch_tickers():
    r = requests.get(URL)
    lines = r.text.splitlines()
    data_lines = lines[1:-1]  # first line is headers, last is a footer nasdaq adds

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["symbol", "name"])
        for line in data_lines:
            parts = line.split("|")
            writer.writerow([parts[0], parts[1]])

    print(f"saved {len(data_lines)} tickers")

if __name__ == "__main__":
    fetch_tickers()