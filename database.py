import sqlite3
from datetime import datetime, timezone
from config import DB_FILE

# makes the table if it doesnt exist yet
def init_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            price REAL,
            checked_at TEXT
        )
    """)
    conn.commit()
    conn.close()


# saves one price reading with a timestamp
def save_price(ticker, price):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO prices (ticker, price, checked_at) VALUES (?, ?, ?)",
        (ticker, price, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()


# gets the last 2 prices for a ticker so we can compare and see if it moved
def get_last_two_prices(ticker):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute(
        "SELECT price FROM prices WHERE ticker = ? ORDER BY checked_at DESC LIMIT 2",
        (ticker,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]