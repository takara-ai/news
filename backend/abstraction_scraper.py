from tools.scrapers.scraper import scrape

scrape_abstraction = {
    "name": "scrape",
    "description": "Scrape the main content of a web page, and return markdown and images in a dictionary.",
    "parameters": {"query": str},
    "returns": dict[str, list[dict[str, str]]],
    "function": scrape
}
