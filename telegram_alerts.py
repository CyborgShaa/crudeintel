# telegram_alerts.py

import requests
import os
from dotenv import load_dotenv

# Load environment variables for local testing
load_dotenv()

# 🧠 Emojis for impact
IMPACT_EMOJI = {
    "Bullish": "🟢",
    "Bearish": "🔴",
    "Neutral": "⚪"
}

# 💬 Crude market effect explanations
IMPACT_EXPLANATION = {
    "Bullish": "This could drive prices up due to tightening supply, geopolitical tension, or positive sentiment.",
    "Bearish": "This may lead to a drop in prices due to oversupply, demand concerns, or bearish economic signals.",
    "Neutral": "This news is unlikely to move the market significantly in the short term."
}

def format_telegram_message(news):
    title = news.get("title", "Untitled")
    source = news.get("source", "Unknown Source")
    link = news.get("link", "#")
    summary = news.get("summary", "Summary not available.")
    impact = news.get("impact", "Neutral").capitalize()
    timestamp = news.get("timestamp").strftime('%b %d, %I:%M %p')

    emoji = IMPACT_EMOJI.get(impact, "⚪")
    effect = IMPACT_EXPLANATION.get(impact, "No additional effect analysis.")

    message = f"""🚨 *{title}*
📰 {source} | 🕒 {timestamp}

📊 *Summary*: {summary}
📈 *Impact*: {emoji} {impact}
🧠 *Effect*: {effect}
🔗 [Read full article]({link})
"""
    return message


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
