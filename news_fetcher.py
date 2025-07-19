# news_fetcher.py

import feedparser
from datetime import datetime
import pytz
import traceback

tz = pytz.timezone("Asia/Kolkata")

RSS_FEEDS = [
    "https://oilprice.com/rss/main",
    "https://feeds.reuters.com/reuters/energyNews",
    "https://www.eia.gov/rss/todayinenergy.xml",
    "https://www.investing.com/rss/news_11.rss",
    "https://energy.einnews.com/all_rss"
]

def fetch_news(limit_per_feed=5):
    articles = []

    for feed_url in RSS_FEEDS:
        try:
            parsed = feedparser.parse(feed_url)

            if not parsed.entries:
                print(f"⚠️ No entries found in: {feed_url}")
                continue

            source_name = parsed.feed.get("title", "Unknown Source")

            for entry in parsed.entries[:limit_per_feed]:
                pub_time = (
                    datetime(*entry.published_parsed[:6]).astimezone(tz)
                    if "published_parsed" in entry
                    else datetime.now(tz)
                )
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "source": source_name,
                    "timestamp": pub_time,
                    "impact": "Neutral"
                })

        except Exception as e:
            print(f"❌ Error fetching {feed_url}: {e}")
            traceback.print_exc()

    return sorted(articles, key=lambda x: x["timestamp"], reverse=True)
