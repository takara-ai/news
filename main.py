from flask import Flask, request, jsonify
from news import fast_article
from utils import generate_news_schema
from json2img import AsyncNewsPresentationMaker
app = Flask(__name__)


@app.route('/get-json2img', methods=['POST'])
def get_json2img():
    # example of input, should be in string format
    '''[
        {
        "title": "AI News",
        "text": "In 2017, blockchain was everyone's focus. Presented as a revolutionary technology, blockcha$
        "source": "TechNews"}
    ]'''
    data = request.get_json()
    payload = data["list_json"]

    try:
        maker = AsyncNewsPresentationMaker(
            openai_key="...",
            fal_key="c95b464d-32a9-4059-b586-eeeafc917469:b0eb0e0cf6f9f5a73d19f779d1e86ef8",
            elevenlabs_key="sk_75fc980fe0800206a73c8fdf36e94246a357acdf7f3ee3c2"
        )
        result = maker.process_json_input(test_json)

        # example of result
        """
        {
        'status': 'success',
        'slides': [
            {'status': 'success',
            'absolute_path': '/Users/alekseibuzovkin/code/news/presentation_output/slide_1751122653_533.png',
            'title': 'AI News',
            'generation_time': 2.1862218379974365}
        ],
        'audio':
        {
            'status': 'success',
            'absolute_path': '/Users/alekseibuzovkin/code/news/presentation_output/audio_1751122659.mp3'
        },
        'output_dir': '/Users/alekseibuzovkin/code/news/presentation_output', 'total_time': 14.2782862186431$
        """
        return jsonify({"results": result["slides"][0]["absolute_path"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-news', methods=['POST'])
def get_news():
    data = request.get_json()

    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400

    prompt = data['prompt']

    try:
        # Get article
        article = fast_article(prompt)
        return jsonify({"results": article}) 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(debug=True)
