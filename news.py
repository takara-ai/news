import re
from agent.core.code_agent import CodeAgent
from agent.core.openai import OpenAIAgent
from agent.tools.web import web_search_tool, parse_webpage_tool
from agent.tools.rss import get_rss_feeds, read_rss_tool

# Get a load of content for writing editorials
def curate_content(query: str, loop_limit: int = 5, model: str = "gpt-4.1-mini") -> str:
    agent = CodeAgent("openai", "content_curator-3", loop_limit=loop_limit, tools=[web_search_tool, parse_webpage_tool, get_rss_feeds, read_rss_tool], model=model)
    return agent(query)

# Create an article from research
def create_article(research: str, model: str = "gpt-4.1-mini") -> str:
    agent = CodeAgent("openai", "editorial_writer-2", loop_limit=loop_limit, tools=[web_search_tool, parse_webpage_tool, get_rss_feeds, read_rss_tool], model=model)   
    return agent(research)

# Create a list of articles from research
def create_articles(research: str, model: str = "gpt-4.1-mini") -> list[str]:
    agent = CodeAgent("openai", "multi-editorial_writer", loop_limit=loop_limit, tools=[web_search_tool, parse_webpage_tool, get_rss_feeds, read_rss_tool], model=model)
    # Transform LLM response into a list of articles# Extract articles from the response
    response = agent(research)
    articles = []
    
    # Find all content between <article> and </article> tags
    article_pattern = r'<article>(.*?)</article>'
    matches = re.findall(article_pattern, response, re.DOTALL)
    
    for match in matches:
        # Strip whitespace and add to articles list
        article_content = match.strip()
        if article_content:  # Only add non-empty articles
            articles.append(article_content)
    
    return articles
    
"""
Testing
"""
if __name__ == "__main__":
    # Get research
    question = "Trending, breaking, hyped tech and AI news"
    research = curate_content(question)
    print(f"\n\n\nRESEARCH:\n{research}\n\n")
    # Create articles
    articles = create_articles(research)
    print(f"\n\n\nARTICLES:\n{articles}\n\n")


