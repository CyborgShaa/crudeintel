# news_fetcher.py

import feedparser
from datetime import datetime
import pytz

# Choose timezone for display (India Standard Time)
tz = pytz.timezone("Asia/Kolkata")

# Add more feeds later
RSS_FEEDS = [
    "https://oilprice.com/rss/main",
    "https://www.reutersagency.com/feed/?best-topics=energy&post_type=best"
]

def fetch_news(limit_per_feed=5):
    articles = []
    
    for feed_url in RSS_FEEDS:
        parsed = feedparser.parse(feed_url)
        
        for entry in parsed.entries[:limit_per_feed]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "source": parsed.feed.title if "title" in parsed.feed else "Unknown",
                "timestamp": datetime(*entry.published_parsed[:6]).astimezone(tz),
                "impact": "Neutral"  # Default tag, AI/logic later
            })
    
    return sorted(articles, key=lambda x: x["timestamp"], reverse=True)
