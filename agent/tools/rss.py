from .Tool import Tool
import reader
from datetime import datetime

def get_rss_feeds() -> list[dict]:
    return [
        # Sports
        {"feed_name": "r/sports", "feed_url": "https://www.reddit.com/r/sports.rss", "category": "sports"},
        {"feed_name": "r/nba", "feed_url": "https://www.reddit.com/r/nba.rss", "category": "sports"},
        {"feed_name": "r/soccer", "feed_url": "https://www.reddit.com/r/soccer.rss", "category": "sports"},
        {"feed_name": "r/nfl", "feed_url": "https://www.reddit.com/r/nfl.rss", "category": "sports"},
        {"feed_name": "r/baseball", "feed_url": "https://www.reddit.com/r/baseball.rss", "category": "sports"},
        # Tech
        {"feed_name": "r/gadgets", "feed_url": "https://www.reddit.com/r/gadgets.rss", "category": "tech"},
        {"feed_name": "r/futurology", "feed_url": "https://www.reddit.com/r/futurology.rss", "category": "tech"},
        {"feed_name": "r/technology", "feed_url": "https://www.reddit.com/r/technology.rss", "category": "tech"},
        {"feed_name": "r/programming", "feed_url": "https://www.reddit.com/r/programming.rss", "category": "tech"},
        {"feed_name": "r/apple", "feed_url": "https://www.reddit.com/r/apple.rss", "category": "tech"},
        # Economics
        {"feed_name": "r/personalfinance", "feed_url": "https://www.reddit.com/r/personalfinance.rss", "category": "economics"},
        {"feed_name": "r/stocks", "feed_url": "https://www.reddit.com/r/stocks.rss", "category": "economics"},
        {"feed_name": "r/Economics", "feed_url": "https://www.reddit.com/r/Economics.rss", "category": "economics"},
        {"feed_name": "r/investing", "feed_url": "https://www.reddit.com/r/investing.rss", "category": "economics"},
        {"feed_name": "r/AskEconomics", "feed_url": "https://www.reddit.com/r/AskEconomics.rss", "category": "economics"},
        # Politics
        {"feed_name": "r/politics", "feed_url": "https://www.reddit.com/r/politics.rss", "category": "politics"},
        {"feed_name": "r/politicaldiscussion", "feed_url": "https://www.reddit.com/r/politicaldiscussion.rss", "category": "politics"},
        {"feed_name": "r/worldpolitics", "feed_url": "https://www.reddit.com/r/worldpolitics.rss", "category": "politics"},
        {"feed_name": "r/conservative", "feed_url": "https://www.reddit.com/r/conservative.rss", "category": "politics"},
        {"feed_name": "r/liberal", "feed_url": "https://www.reddit.com/r/liberal.rss", "category": "politics"},
        # World News
        {"feed_name": "r/worldnews", "feed_url": "https://www.reddit.com/r/worldnews.rss", "category": "world"},
        {"feed_name": "r/news", "feed_url": "https://www.reddit.com/r/news.rss", "category": "world"},
        {"feed_name": "r/Europe", "feed_url": "https://www.reddit.com/r/Europe.rss", "category": "world"},
        {"feed_name": "r/Asia", "feed_url": "https://www.reddit.com/r/Asia.rss", "category": "world"},
        {"feed_name": "r/internationalnews", "feed_url": "https://www.reddit.com/r/internationalnews.rss", "category": "world"}
    ]
get_rss_feeds = Tool({
    "get_rss_feeds",
    "return a list of some available RSS feeds",
    None,
    list[dict],
    get_rss_feeds
})

# Get RSS feed content
def get_rss_content(rss_url: str) -> list[dict[str, str]]:
    try:
        r = reader.make_reader()
        
        r.add_feed(rss_url)

        r.update_feeds()
        
        entries = list(r.get_entries())
        
        feed_content = []
        for entry in entries:
            if entry.published:
                date_str = entry.published.strftime("%Y-%m-%d")
            elif entry.updated:
                date_str = entry.updated.strftime("%Y-%m-%d")
            else:
                date_str = datetime.now().strftime("%Y-%m-%d")
            
            feed_content.append({
                "title": entry.title or "",
                "date": date_str,
                "url": entry.link or ""
            })
        
        return feed_content
        
    except Exception as e:
        print(f"Error parsing RSS feed {rss_url}: {str(e)}")
        return []
read_rss_tool = Tool(
    "read_rss_tool",
    "Read an RSS feed and return a list of articles with title, date, and URL.",
    {"rss_url": str},
    list[dict[str, str]],
    get_rss_contents
)