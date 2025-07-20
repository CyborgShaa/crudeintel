import streamlit as st
from datetime import datetime
import pytz
import time

from news_fetcher import fetch_news
from newsapi_fetcher import fetch_newsapi_articles
from telegram_alerts import send_telegram_alert
from summarizer import analyze_news  # 🧠 AI summarizer

# Set timezone for India (Kolkata)
tz = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(tz).strftime('%b %d, %I:%M %p')

# Streamlit UI setup
st.set_page_config(page_title="CrudeIntel News Engine", layout="centered")
st.title("🛢️ CrudeIntel - Oil Market News")
st.markdown("Get live and impactful crude oil market news in one place.")
st.caption(f"🔄 Last updated: {current_time}")
st.divider()

# Impact emoji mapping for news
impact_emojis = {
    "Bullish": "🟢",
    "Bearish": "🔴",
    "Neutral": "⚪"
}

# 🔍 Keywords for automatic alerts
ALERT_KEYWORDS = [
    "opec", "iran", "fed", "sanction", "inventory", "reserve",
    "pipeline", "cut", "strike", "production", "conflict"
]

# Auto-refresh setup (in minutes)
AUTO_REFRESH_MINUTES = 5

# Fetch news from RSS + NewsAPI
rss_articles = fetch_news(limit_per_feed=5)
api_articles = fetch_newsapi_fetcher(query="crude oil OR OPEC OR inventory", limit=5)
news_data = sorted(rss_articles + api_articles, key=lambda x: x["timestamp"], reverse=True)

# ✅ Filter out broken timestamps and old news
news_data = [n for n in news_data if isinstance(n["timestamp"], datetime)]
news_data = [n for n in news_data if (datetime.now(tz) - n["timestamp"]).total_seconds() <= 86400]

# Track alerted articles (in session)
if "alerted_titles" not in st.session_state:
    st.session_state.alerted_titles = set()

# 🔁 Display news + handle alert logic
for news in news_data:
    title_lower = news["title"].lower()
    matched = any(keyword in title_lower for keyword in ALERT_KEYWORDS)

    # 🧠 AI summarization
    summary, ai_impact = analyze_news(news["title"])

    # ✅ Check if the news is recent (within 600 minutes, ~10 hrs)
    news_age_minutes = (datetime.now(tz) - news["timestamp"]).total_seconds() / 60

    if matched and news["title"] not in st.session_state.alerted_titles and news_age_minutes <= 600:
        message = f"🚨 *{news['title']}*\n📌 {summary or 'No summary'}\n📰 {news['source']} | 🕒 {news['timestamp'].strftime('%b %d, %I:%M %p')}\n🔗 {news['link']}"
        send_telegram_alert(message)
        st.session_state.alerted_titles.add(news["title"])

    # Show on Streamlit UI
    st.markdown(f"### {impact_emojis.get(ai_impact, '⚪')} [{news['title']}]({news['link']})")
    st.caption(f"🕒 {news['timestamp'].strftime('%b %d, %I:%M %p')} | 📰 {news['source']}")
    st.markdown(f"**Summary**: {summary or 'N/A'}")
    st.markdown("---")

# 🧪 Test button for manual Telegram alerts
if st.button("Send Test Alert to Telegram"):
    send_telegram_alert("🚨 This is a test alert from CrudeIntel (auto-alert system live).")

# ⏱️ Auto-refresh every X minutes
time.sleep(AUTO_REFRESH_MINUTES * 60)
st.experimental_rerun()
