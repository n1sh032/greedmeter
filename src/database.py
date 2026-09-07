import sqlite3
from datetime import datetime, timezone
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "data", "prices.db")


def init_db():
    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_chat_id TEXT UNIQUE,
            created_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            ticker TEXT,
            threshold_percent REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            price REAL,
            checked_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS alert_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            ticker TEXT,
            alerted_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# --- users ---

def add_user(telegram_chat_id):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT OR IGNORE INTO users (telegram_chat_id, created_at) VALUES (?, ?)",
        (telegram_chat_id, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()


def get_all_users():
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute("SELECT id, telegram_chat_id FROM users").fetchall()
    conn.close()
    return rows  # list of (user_id, telegram_chat_id)


# --- watchlist ---

def add_to_watchlist(user_id, ticker, threshold_percent):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO watchlist (user_id, ticker, threshold_percent) VALUES (?, ?, ?)",
        (user_id, ticker, threshold_percent)
    )
    conn.commit()
    conn.close()


def get_watchlist_for_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    rows = conn.execute(
        "SELECT ticker, threshold_percent FROM watchlist WHERE user_id = ?",
        (user_id,)
    ).fetchall()
    conn.close()
    return rows  # list of (ticker, threshold_percent)


# --- prices (unchanged, shared across all users) ---

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


# --- alerts (now per-user) ---

def get_last_alert_time(user_id, ticker):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute(
        "SELECT alerted_at FROM alert_log WHERE user_id = ? AND ticker = ? ORDER BY alerted_at DESC LIMIT 1",
        (user_id, ticker)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def record_alert(user_id, ticker):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "INSERT INTO alert_log (user_id, ticker, alerted_at) VALUES (?, ?, ?)",
        (user_id, ticker, datetime.now(timezone.utc).isoformat())
    )
    conn.commit()
    conn.close()

def remove_from_watchlist(user_id, ticker):
    conn = sqlite3.connect(DB_FILE)
    conn.execute(
        "DELETE FROM watchlist WHERE user_id = ? AND ticker = ?",
        (user_id, ticker)
    )
    conn.commit()
    conn.close()