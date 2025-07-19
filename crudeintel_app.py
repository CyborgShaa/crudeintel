import streamlit as st
from datetime import datetime
import pytz

from news_fetcher import fetch_news
from newsapi_fetcher import fetch_newsapi_articles
from telegram_alerts import send_telegram_alert

# Timezone
tz = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(tz).strftime('%b %d, %I:%M %p')

# Streamlit UI config
st.set_page_config(page_title="CrudeIntel News Engine", layout="centered")
st.title("🛢️ CrudeIntel - Oil Market News")
st.markdown("Get live and impactful crude oil market news in one place.")
st.caption(f"🔄 Last updated: {current_time}")
st.divider()

# Impact emoji mapping
impact_emojis = {
    "Bullish": "🟢",
    "Bearish": "🔴",
    "Neutral": "⚪"
}

# 🔍 Keywords to auto-alert on
ALERT_KEYWORDS = [
    "opec", "iran", "fed", "sanction", "inventory", "reserve",
    "pipeline", "cut", "strike", "production", "conflict"
]

# Fetch from RSS + NewsAPI
rss_articles = fetch_news(limit_per_feed=5)
api_articles = fetch_newsapi_articles(query="crude oil OR OPEC OR inventory", limit=5)
news_data = sorted(rss_articles + api_articles, key=lambda x: x["timestamp"], reverse=True)

# Track already-alerted articles (for this run)
alerted_articles = []

# 🔁 Display news + alert logic
for news in news_data:
    title_lower = news["title"].lower()
    matched = any(keyword in title_lower for keyword in ALERT_KEYWORDS)

    # ✅ Auto-send alert if keyword matched
    if matched and news["title"] not in alerted_articles:
        message = f"🚨 *{news['title']}*\n📰 {news['source']} | 🕒 {news['timestamp'].strftime('%b %d, %I:%M %p')}\n🔗 {news['link']}"
        send_telegram_alert(message)
        alerted_articles.append(news["title"])

    # Display in app
    st.markdown(f"### {impact_emojis.get(news['impact'], '⚪')} [{news['title']}]({news['link']})")
    st.caption(f"🕒 {news['timestamp'].strftime('%b %d, %I:%M %p')} | 📰 {news['source']}")
    st.markdown("---")

# 🧪 Manual test button
if st.button("Send Test Alert to Telegram"):
    send_telegram_alert("🚨 This is a test alert from CrudeIntel (auto-alert system live).")
