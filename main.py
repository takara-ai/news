from flask import Flask, request, jsonify
from news import curate_content, create_article, create_articles
from utils import generate_news_schema
app = Flask(__name__)

@app.route('/get-news', methods=['POST'])
def get_news():
    data = request.get_json()

    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400

    prompt = data['prompt']

    try:
        # Research
        research = curate_content(prompt)
        # Create articles
        article = create_article(research)
        # Structure articles
        structured_article=generate_news_schema(content=article)
        return jsonify({"results": structured_article}), 200
        return jsonify({"results": structured_article}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
