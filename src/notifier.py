import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


def send_alert(message, chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"telegram failed: {response.text}")
    except Exception as e:
        print(f"couldnt send alert: {e}")