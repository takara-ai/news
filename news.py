from agent.core.code_agent import CodeAgent
from agent.core.openai import OpenAIAgent
from agent.tools.web import web_search_tool, parse_webpage_tool

# Get a load of content for writing editorials
def curate_content(query: str) -> str:
    agent = CodeAgent("openai", "content_curator-3", loop_limit=10, tools=[web_search_tool, parse_webpage_tool], model="gpt-4.1-mini")
    return agent(query)

# Create an article from research
def create_article(research: str, model: str = "gpt") -> str:
    if model == "gpt":
        agent = CodeAgent("openai", "editorial_writer-2", loop_limit=10, tools=[web_search_tool, parse_webpage_tool], model="gpt-4.1-mini")   
    elif model == "gemini":
        agent = CodeAgent("google", "editorial_writer-2", loop_limit=10, tools=[web_search_tool, parse_webpage_tool], model="gemini-2.5-pro")
    return agent(research)

if __name__ == "__main__":
    question = "Breaking, hype tech news about AI" # Test question
    research = curate_content(question)
    print(research)
    agent = CodeAgent("google", "editorial_writer-2", loop_limit=10, tools=[web_search_tool, parse_webpage_tool], model="gemini-2.5-pro")
    print(f"System Prompt: {code_agent.system_prompt}")
    agent(research, debug=True, eval_check=True)
    print(f"\n\nANSWER: {article}\n\n")
    #article = create_article(question, "gemini")
    print(article)
