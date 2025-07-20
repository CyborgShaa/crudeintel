# telegram_alerts.py

import requests
import os
from dotenv import load_dotenv

# Load environment variables for local testing
load_dotenv()

def send_telegram_alert(message: str):
    # Loop over 3 bot-token/chat-id pairs
    for i in [1, 2, 3]:
        token = os.getenv(f"TELEGRAM_BOT_TOKEN_{i}")
        chat_id = os.getenv(f"TELEGRAM_CHAT_ID_{i}")

        if not token or not chat_id:
            print(f"⚠️ Bot {i} credentials missing. Skipping.")
            continue

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                print(f"✅ Alert sent via Bot {i} → Chat ID: {chat_id}")
            else:
                print(f"❌ Bot {i} Error: {response.status_code} → {response.text}")
        except Exception as e:
            print(f"❌ Exception sending alert via Bot {i}: {e}")
