# news_fetcher.py

import feedparser
from datetime import datetime
import pytz

# Set timezone for India
tz = pytz.timezone("Asia/Kolkata")

# ✅ Elite Crude-Only Source List
RSS_FEEDS = {
    "OilPrice": "https://oilprice.com/rss/main",
    "Reuters Energy": "https://feeds.reuters.com/reuters/USenergyNews",
    "CNBC Energy": "https://www.cnbc.com/id/19836768/device/rss/rss.html",
    "World Oil": "https://www.worldoil.com/rss/news/",
    "EIA": "https://www.eia.gov/rss/news.xml",
    "Investing - Commodities": "https://www.investing.com/rss/news_11.rss",
    "S&P Global": "https://www.spglobal.com/commodityinsights/en/rss",
    "Bloomberg Energy": "https://www.bloomberg.com/rss/energy"
}

# ✅ Crude oil filter terms — skip everything else
CRUDE_KEYWORDS = [
    # Core crude terms
    "crude oil", "brent", "wti", "opec", "opec+",

    # Price & market dynamics
    "oil price", "oil futures", "crude futures", "oil market",
    "barrel price", "oil benchmark",

    # Production & supply
    "oil production", "crude production", "oil supply", "oil inventories",
    "shale oil", "oil output", "oil drilling", "crude exports",

    # Geopolitical, policy & infrastructure
    "oil sanctions", "oil embargo", "oil pipeline", "crude demand",
    "oil refinery", "oil rig", "petroleum",

    # Optional: Specific crude types
    "light sweet crude", "heavy crude", "sour crude", "shale crude", "offshore oil"
]

def is_crude_related(text: str) -> bool:
    return any(word in text.lower() for word in CRUDE_KEYWORDS)

def fetch_news(limit_per_feed=6):
    all_articles = []

    for source_name, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            entries = feed.entries[:limit_per_feed]

            for entry in entries:
                title = entry.title.strip()
                link = entry.link.strip()
                published = entry.get("published", "") or entry.get("pubDate", "")
                description = entry.get("summary", "") or ""

                # 🛢️ Filter for crude-related titles or summaries
                if not is_crude_related(title + " " + description):
                    continue  # Skip non-crude content

                # Parse time (safe fallback)
                try:
                    parsed_time = datetime(*entry.published_parsed[:6])
                    parsed_time = pytz.utc.localize(parsed_time).astimezone(tz)
                except:
                    parsed_time = datetime.now(tz)

                # Final cleaned article
                all_articles.append({
                    "title": title,
                    "link": link,
                    "timestamp": parsed_time,
                    "source": source_name,
                    "impact": "Neutral"  # AI will set this
                })

        except Exception as e:
            print(f"❌ Failed to parse {source_name}: {e}")

    return all_articles
