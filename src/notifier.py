import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"telegram failed: {response.text}")
    except Exception as e:
        print(f"couldnt send alert: {e}")


def send_all_alerts(alerts):
    for alert in alerts:
        send_alert(alert)


if __name__ == "__main__":
    send_alert("test message from greedmeter")