# GreedMeter 📊

A stock price watchlist and alert tool. Add tickers through a web dashboard, set a
custom alert threshold for each one, and get pinged on Telegram when a stock moves
enough to matter — without needing to babysit the market yourself.

## Why I built this

I wanted a project that went beyond calling an API and printing a result — something
that touched real systems concerns: persistent storage, scheduled background jobs,
per-user data modeling, and a working notification pipeline end to end. Stocks were a
good fit because the data's free and public, and "did this move enough to notice" is a
genuinely useful, easy-to-explain problem.

## Features

- **Custom watchlists** — search any US-listed stock by name or ticker and add it
- **Per-ticker alert thresholds** — a volatile stock like TSLA and a stable one like KO
  don't need the same % threshold to be "notable," so each ticker has its own
- **Alert cooldowns** — once a ticker fires an alert, it won't fire again for 4 hours,
  so you get notified, not spammed
- **Telegram notifications** — alerts arrive as a direct message the moment they fire
- **Automatic background checks** — runs on a schedule (every 5 minutes) via Windows
  Task Scheduler, no need to keep a terminal open
- **Multi-user data model** — the database supports multiple users, each with their own
  watchlist and thresholds, even though it currently runs for a single person locally
- **Web dashboard** — add, view, and remove watchlist tickers through a browser instead
  of editing config files or the database by hand

## Tech stack

- **Python** — core logic
- **yfinance** — live and historical stock price data
- **SQLite** — local persistent storage for users, watchlists, and price history
- **Flask** — the web dashboard
- **Telegram Bot API** — notifications
- **Windows Task Scheduler** — automated recurring runs

## Architecture

```
greedmeter/
├── src/
│   ├── config.py           # shared settings (cooldown length, etc.)
│   ├── price_fetcher.py    # talks to yfinance
│   ├── database.py         # all SQLite reads/writes
│   ├── alert_checker.py    # decides if a price move is alert-worthy
│   ├── notifier.py         # sends Telegram messages
│   ├── logger.py           # human-readable activity log
│   ├── main.py             # scheduled entry point: fetch → save → check → alert
│   ├── app.py              # Flask dashboard
│   ├── setup_user.py       # one-off script to register a user
│   ├── fetch_ticker_list.py# downloads the full US ticker list from NASDAQ
│   └── templates/
│       └── dashboard.html
├── data/
│   ├── prices.db           # generated, gitignored
│   └── tickers.csv         # full searchable ticker list
├── logs/
│   └── activity.log        # generated, gitignored
├── requirements.txt
└── .env                    # Telegram bot token, gitignored
```

**Why prices are stored per-check, not overwritten:** every price reading is saved as
its own timestamped row rather than replacing a single "current price" field. This
means the database doubles as a real historical dataset, which matters for comparing
consecutive readings (to detect a move) and would be the foundation for any future
backtesting or trend analysis.

**Why timestamps are stored in UTC:** avoids daylight-saving and timezone bugs when
comparing two readings taken hours apart. The dashboard/logs convert to local time only
for display.

**Why alerts are per-user, not global:** two different users watching the same stock
shouldn't share one cooldown clock — each person's alert history is tracked separately,
even though the underlying price data itself is shared (no need to fetch AAPL's price
twice just because two people are watching it).

## Setup

```bash
git clone https://github.com/n1sh032/greedmeter.git
cd greedmeter
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
TELEGRAM_TOKEN=your_bot_token_here
```

Get a bot token by messaging **@BotFather** on Telegram and following its prompts.

Register yourself as a user and set an initial watchlist:
```bash
python src/setup_user.py
```
(edit the chat ID and starting tickers inside that file first — see comments)

Download the full ticker list (needed for the dashboard's search feature):
```bash
python src/fetch_ticker_list.py
```

Run a manual price check:
```bash
python src/main.py
```

Launch the dashboard:
```bash
python src/app.py
```
then open `http://127.0.0.1:5000` in your browser.

For automatic recurring checks, set up Task Scheduler (Windows) to run
`python src/main.py` every 5–15 minutes.

## Known limitations / future improvements

- Currently single-user in practice (runs locally on one machine), though the
  database is already structured to support multiple users
- No authentication/login system — adding real users would need this before any
  public deployment
- Runs only while the machine is on; a cloud deployment would allow true 24/7 monitoring
- No news/context on *why* a stock moved — a natural next step would be surfacing
  headlines or sentiment alongside a price alert
- Insights/trend analysis tab planned but not yet built

## Screenshots

*(add 2–3 screenshots of the dashboard here before publishing)*
