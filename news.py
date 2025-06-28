from agent.core.code_agent import CodeAgent
from agent.core.openai import OpenAIAgent
from agent.tools.web import web_search_tool, parse_webpage_tool
from agent.tools.rss import get_rss_feeds, read_rss_tool

# Get a load of content for writing editorials
def curate_content(query: str, model: str = "gpt-4.1-mini") -> str:
    agent = CodeAgent("openai", "content_curator-3", loop_limit=10, tools=[web_search_tool, parse_webpage_tool, get_rss_feeds, read_rss_tool], model=model)
    return agent(query)

# Create an article from research
def create_article(research: str, model: str = "gpt-4.1-mini") -> str:
    agent = CodeAgent("openai", "editorial_writer-2", loop_limit=10, tools=[web_search_tool, parse_webpage_tool, get_rss_feeds, read_rss_tool], model=model)   
    return agent(research)
