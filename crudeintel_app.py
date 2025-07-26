import streamlit as st

# UptimeRobot ping check
if st.query_params.get("uptime") == "1":
    st.write("Ping OK")
    st.stop()

from datetime import datetime
import pytz
import time

from news_fetcher import fetch_news
from newsapi_fetcher import fetch_newsapi_articles
from telegram_alerts import send_telegram_alert, format_telegram_message
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

# Emoji mapping for Streamlit UI
impact_emojis = {
    "Bullish": "🟢",
    "Bearish": "🔴",
    "Neutral": "⚪"
}

# Auto-refresh setup
AUTO_REFRESH_MINUTES = 5
MAX_NEWS_AGE_MINUTES = 60  # Alert window reduced to 60 mins

# Fetch from sources
rss_articles = fetch_news(limit_per_feed=5)
api_articles = fetch_newsapi_articles(query="crude oil OR OPEC OR inventory", limit=5)
news_data = sorted(rss_articles + api_articles, key=lambda x: x["timestamp"], reverse=True)

# Valid timestamp + last 24h news
news_data = [n for n in news_data if isinstance(n["timestamp"], datetime)]
news_data = [n for n in news_data if (datetime.now(tz) - n["timestamp"]).total_seconds() <= 86400]

# Track sent alerts
if "alerted_titles" not in st.session_state:
    st.session_state.alerted_titles = set()

# Loop and process each news
for news in news_data:
    # AI summarization
    summary, impact = analyze_news(news["title"], news.get("description", ""), provider="gemini")
    news["summary"] = summary
    news["impact"] = impact

    # Alert condition: only Bullish/Bearish + under 60 minutes old
    news_age_minutes = (datetime.now(tz) - news["timestamp"]).total_seconds() / 60
    if impact in ["Bullish", "Bearish"] and news["title"] not in st.session_state.alerted_titles and news_age_minutes <= MAX_NEWS_AGE_MINUTES:
        message = format_telegram_message(news)
        send_telegram_alert(message)
        st.session_state.alerted_titles.add(news["title"])

    # Show on UI
    st.markdown(f"### {impact_emojis.get(impact, '⚪')} [{news['title']}]({news['link']})")
    st.caption(f"🕒 {news['timestamp'].strftime('%b %d, %I:%M %p')} | 📰 {news['source']}")
    st.markdown(f"**Summary**: {summary or 'N/A'}")
    st.markdown("---")

# Test alert button
if st.button("Send Test Alert to Telegram"):
    send_telegram_alert("🚨 This is a test alert from CrudeIntel (auto-alert system live).")

# Auto-refresh every 5 mins
time.sleep(AUTO_REFRESH_MINUTES * 60)
st.rerun()
