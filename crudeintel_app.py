import streamlit as st
from datetime import datetime
import pytz

from news_fetcher import fetch_news
from newsapi_fetcher import fetch_newsapi_articles
from telegram_alerts import send_telegram_alert

# Define emoji mapping for impact tags
impact_emojis = {
    "Bullish": "🟢",
    "Bearish": "🔴",
    "Neutral": "⚪"
}

# Set timezone for refresh time
tz = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(tz).strftime('%b %d, %I:%M %p')

# Streamlit UI setup
st.set_page_config(page_title="CrudeIntel News Engine", layout="centered")
st.title("🛢️ CrudeIntel - Oil Market News")
st.markdown("Get live and impactful crude oil market news in one place.")
st.caption(f"🔄 Last updated: {current_time}")
st.divider()

# 🔁 Fetch news from both sources
rss_articles = fetch_news(limit_per_feed=5)
api_articles = fetch_newsapi_articles(query="crude oil OR OPEC OR inventory", limit=5)
news_data = sorted(rss_articles + api_articles, key=lambda x: x["timestamp"], reverse=True)

# Display news cards
for news in news_data:
    st.markdown(f"### {impact_emojis.get(news['impact'], '⚪')} [{news['title']}]({news['link']})")
    st.caption(f"🕒 {news['timestamp'].strftime('%b %d, %I:%M %p')} | 📰 {news['source']}")
    st.markdown("---")

# Optional test alert
if st.button("Send Test Alert to Telegram"):
    send_telegram_alert("🚨 This is a test alert from CrudeIntel (NewsAPI + RSS combined).")
