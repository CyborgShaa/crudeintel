import streamlit as st
from datetime import datetime
from news_fetcher import fetch_news

# Impact emoji tags
impact_emojis = {
    "Bullish": "🟢",
    "Bearish": "🔴",
    "Neutral": "⚪"
}

# Streamlit config
st.set_page_config(page_title="CrudeIntel News Engine", layout="centered")

st.title("🛢️ CrudeIntel - Oil Market News")
st.markdown("Get live and impactful crude oil market news in one place.")
st.divider()

# Fetch real articles from RSS feeds
news_data = fetch_news()

# Display each news item
for news in news_data:
    st.markdown(f"### {impact_emojis.get(news['impact'], '⚪')} [{news['title']}]({news['link']})")
    st.caption(f"🕒 {news['timestamp'].strftime('%b %d, %I:%M %p')} | 📰 {news['source']}")
    st.markdown("---")

# Optional test alert button
from telegram_alerts import send_telegram_alert

if st.button("Send Test Alert to Telegram"):
    send_telegram_alert("🚨 This is a test alert from CrudeIntel using live news!")
