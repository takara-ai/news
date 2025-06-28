from flask import Flask, request, jsonify
from agent.core.code_agent import CodeAgent
from agent.core.openai import OpenAIAgent
from agent.tools.web import web_search_tool, parse_webpage_tool
from utils import generate_news_schema
app = Flask(__name__)

@app.route('/get-news', methods=['POST'])
def get_news():
    data = request.get_json()

    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400

    prompt = data['prompt']

    try:
        content_creation_agent = CodeAgent("openai", "content_curator-2", loop_limit=10, tools=[web_search_tool, parse_webpage_tool], model="gpt-4.1")
        #print(content_creation_agent.system_prompt)
        raws_articles = content_creation_agent(prompt, debug=True, eval_check=True)
        #print(f"\n\nANSWER: {answer}\n\n")
        pause = input("\nContinue?:\n")
        structured_artcile=generate_news_schema(content=raws_articles)
        return jsonify({"results": structured_artcile}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
