from tools.scrapers.scraper import scrape
from tools.scrapers.rss_parse import get_feed_contents

scrape_abstraction = {
    "name": "scrape",
    "description": "Scrape the main content of a web page, and return markdown and images in a dictionary.",
    "parameters": {"query": str},
    "returns": dict[str, list[dict[str, str]]],
    "function": scrape
}

rss_feed_read_abstraction = {
    "name": "rss_feed_read",
    "description": "Read an RSS feed and return a list of articles with title, date, and URL.",
    "parameters": {"rss_url": str},
    "returns": list[dict[str, str]],
    "function": get_feed_contents
}