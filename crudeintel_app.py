import streamlit as st
from datetime import datetime, timedelta

# Dummy news data for testing
news_data = [
    {
        "title": "OPEC+ Agrees to Extend Production Cuts",
        "source": "Reuters",
        "timestamp": datetime.now() - timedelta(minutes=5),
        "impact": "Bullish"
    },
    {
        "title": "US Crude Inventories Rise Sharply",
        "source": "EIA",
        "timestamp": datetime.now() - timedelta(hours=1),
        "impact": "Bearish"
    },
    {
        "title": "Oil Prices Remain Stable Amid Geopolitical Tensions",
        "source": "OilPrice",
        "timestamp": datetime.now() - timedelta(hours=2),
        "impact": "Neutral"
    },
]

# Emoji tags for impact
impact_emojis = {
    "Bullish": "🟢",
    "Bearish": "🔴",
    "Neutral": "⚪"
}

st.set_page_config(page_title="CrudeIntel News Engine", layout="centered")

st.title("🛢️ CrudeIntel - Oil Market News")
st.markdown("Get live and impactful crude oil market news in one place.")

st.divider()

# Display news cards
for news in news_data:
    st.markdown(f"### {impact_emojis[news['impact']]} {news['title']}")
    st.caption(f"🕒 {news['timestamp'].strftime('%b %d, %I:%M %p')} | 📰 {news['source']}")
    st.markdown("---")

from telegram_alerts import send_telegram_alert

if st.button("Send Test Alert to Telegram"):
    send_telegram_alert("🚨 This is a test alert from CrudeIntel!")
  
