from agent.core.code_agent import CodeAgent
from agent.core.openai import OpenAIAgent
from agent.tools.web import web_search_tool, parse_webpage_tool

if __name__ == "__main__":
    # Initialise agent:
    content_creation_agent = CodeAgent("openai", "content_curator-2", loop_limit=10, tools=[web_search_tool, parse_webpage_tool], model="gpt-4.1")
    question = "Breaking, hype tech news about AI" # Test question
    print(content_creation_agent.system_prompt)
    answer = content_creation_agent(question, debug=True, eval_check=True)
    print(f"\n\nANSWER: {answer}\n\n")
    pause = input("\nContinue?:\n")
