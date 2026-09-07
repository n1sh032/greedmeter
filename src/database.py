import sqlite3
from datetime import datetime, timezone
from config import DB_FILE

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


def save_price(ticker, price):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO prices (ticker, price, checked_at) VALUES (?, ?, ?)",
        (ticker, price, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()


def get_last_two_prices(ticker):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute(
        "SELECT price FROM prices WHERE ticker = ? ORDER BY checked_at DESC LIMIT 2",
        (ticker,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


def init_alerts_table():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS alert_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            alerted_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_last_alert_time(ticker):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute(
        "SELECT alerted_at FROM alert_log WHERE ticker = ? ORDER BY alerted_at DESC LIMIT 1",
        (ticker,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def record_alert(ticker):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO alert_log (ticker, alerted_at) VALUES (?, ?)",
        (ticker, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()