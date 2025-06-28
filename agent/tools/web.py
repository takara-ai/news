import requests
import reader
from duckduckgo_search import DDGS
import markdownify
from readability import Document
from bs4 import BeautifulSoup
from .Tool import Tool

# Fetch up-to-date information from the internet.
def web_search(query: str) -> list[dict]:
    try:
        results = DDGS().text(query, max_results=10)
        if not results:
            return [{"title": "No Results", "url": ""}]
        # DuckDuckGo results have 'href' for URLs
        return [{"title": result.get("title", ""), "url": result.get("href", "")} for result in results]
    except Exception as e:
        return [{"title": "Error", "url": "", "error": str(e)}]
web_search_tool = Tool(
    "web_search_tool",
    "Search the web using DuckDuckGo. Returns a list of up to 10 results, each containing 'title' and 'url' fields. Use parse_webpage to fetch content from specific URLs. Returns a single error result if search fails or no results found.",
    {"query": str},
    list[dict],
    web_search
)

# Fetch information from a webpage based on its url
def parse_webpage(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, timeout=20, headers=headers)
        response.raise_for_status()
        
        document = Document(response.text)
        summary = document.summary()
        soup = BeautifulSoup(summary, "html.parser")
        # Only return first 10,000 characters
        markdown = markdownify.markdownify(soup.prettify()).strip()[0:10000]
        return markdown
    except requests.RequestException as e:
        return f"Error fetching webpage: {str(e)}"
    except Exception as e:
        return f"Error processing webpage: {str(e)}"
parse_webpage_tool = Tool(
    "parse_webpage_tool",
    "Visit a webpage and extract its main content. Uses readability to focus on the primary content, converts HTML to markdown, and limits output to 10,000 characters. Returns error message if fetch or processing fails.",
    {"url": str},
    str,
    parse_webpage
)

## TEST
if __name__ == "__main__":
    print(web_search("breaking AI technology news 2024"))