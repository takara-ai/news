from agents import Agent, Runner, WebSearchTool
import os
from dotenv import load_dotenv
import re
import asyncio
from agent.core.code_agent import CodeAgent
from agent.core.openai import OpenAIAgent
from agent.tools.web import web_search_tool, parse_webpage_tool
from agent.tools.rss import get_rss_feeds, read_rss_tool

# Load openAI API key
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
if not key:
    raise EnvironmentError("OPENAI_API_KEY is not in environment variables. Check .env")

# Faster article generation
async def fast_article_generation(query: str) -> str:
    editorial_writer = Agent(
        name="editorial agent",
        instructions=("You are an expert article editorial writer and news writer for 'The New World Times'. You will be given a research report for a topic of interest and must produce some, full length article from this research. You should do further independent research to ensure a proper understanding"),
        tools = [
            WebSearchTool()
        ]
    )
    content_curator = Agent(
        name="New York Times Content Curator",
        instructions=(
            "You are an expert content curator for the new york times. You will be given a users natural language explanation of what content they want to see. You must then create a research report with sources. This report will then be sent to an editorial written to write a full length article on your point of research for a news article."
            "When you have finished your research, hand off to the editorial agent"
        ),
        handoffs=[editorial_writer],
        tools=[
            WebSearchTool()
        ],
    )
    result = await Runner.run(content_curator, query)
    return result.final_output

# Get a load of content for writing editorials
def curate_content(query: str, loop_limit: int = 10, model: str = "gpt-4.1-mini", custom_agent = None) -> str:
    if custom_agent:
        agent = custom_agent
    else:
        agent = CodeAgent("openai", "content_curator-2", loop_limit=loop_limit, tools=[web_search_tool, parse_webpage_tool, get_rss_feeds, read_rss_tool], model=model)
    return agent(query)

# Create an article from research
def create_article(research: str, loop_limit: int = 5, model: str = "gpt-4.1-mini", custom_agent = None) -> str:
    if custom_agent:
        agent = custom_agent
    else:
        agent = CodeAgent("openai", "editorial_writer-2", loop_limit=loop_limit, tools=[web_search_tool, parse_webpage_tool, get_rss_feeds, read_rss_tool], model=model)   
    return agent(research)

# Create a list of articles from research
def create_articles(research: str, loop_limit: int = 5, model: str = "gpt-4.1-mini", custom_agent = None) -> list[str]:
    if custom_agent:
        agent = custom_agent
    else:
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

# Fast articles
def fast_article(topic: str) -> str:
    return asyncio.run(fast_article_generation(topic))
"""
Testing
"""
if __name__ == "__main__":
    # Properly run async function using asyncio.run()
    asyncio.run(fast_article_generation("Trending, breaking, hyped tech and AI news"))
    """
    # Get research
    question = "Trending, breaking, hyped tech and AI news"
    research = curate_content(question, model="gpt-4.1")
    print(f"\n\n\nRESEARCH:\n{research}\n\n")
    # Create articles
    article = create_article(research, model="gpt-4.1")
    print(f"\n\n\nARTICLE:\n{article}\n\n")
    """

