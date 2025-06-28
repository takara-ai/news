from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import json

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client to use the Exa API
client = OpenAI(
  base_url="https://api.exa.ai",
  api_key="cb08f448-d861-4467-86a5-1036fb4f2112",
)

def generate_article_with_images(prompt: str) -> dict:
    """
    Generates a news article using the Exa API via the OpenAI client,
    with structured output and dynamic title/image extraction.
    """
    try:
        # Read the article system prompt
        with open("ArticleSystemPrompt.txt", "r") as f:
            article_prompt = f.read()

        # Call the Exa API with structured output schema
        completion = client.chat.completions.create(
            model="exa",
            messages=[
                {"role": "system", "content": article_prompt},
                {"role": "user", "content": prompt}
            ],
            extra_body={
                "text": True,
                "output_schema": {
                    "description": "Schema describing an article with title, content, and optional images",
                    "type": "object",
                    "required": ["title", "content"],
                    "additional_properties": False,
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the article"
                        },
                        "header_image": {
                            "type": "string",
                            "description": "Optional URL or reference to the header image"
                        },
                        "content": {
                            "type": "string",
                            "description": "The main content of the article"
                        },
                        "middle_image": {
                            "type": "string",
                            "description": "Optional URL or reference to an image placed in the middle of the article"
                        },
                        "additional_content": {
                            "type": "string",
                            "description": "Optional additional content for the article"
                        }
                    }
                }
            }
        )

        # Extract the structured response
        response_data = completion.choices[0].message.content

        # Quick fix: Remove leading ```json if present
        if response_data.strip().startswith("```json"):
            response_data = re.sub(r"^```json\s*", "", response_data.strip())
            # Also remove trailing triple backticks if present
            response_data = re.sub(r"\s*```$", "", response_data.strip())

        # Get citations from the message object
        citations = []
        if hasattr(completion.choices[0].message, 'citations') and completion.choices[0].message.citations:
            citations = completion.choices[0].message.citations
        
        print("Citations found:", len(citations))
        if citations:
            print("First citation:", citations[0])
        
        # Try to parse the structured response as JSON
        try:
            # Attempt to extract the first JSON object from the response
            json_match = re.search(r'\{[\s\S]*\}', response_data)
            if json_match:
                json_str = json_match.group(0)
                article_data = json.loads(json_str)
                print("Successfully parsed JSON response:", article_data.keys())
            else:
                # If no JSON object found, try to parse as is
                article_data = json.loads(response_data)
                print("Successfully parsed JSON response (no regex):", article_data.keys())
        except json.JSONDecodeError:
            print("Failed to parse JSON, treating as plain text")
            # Fallback: treat as plain text and structure it
            article_data = {
                "title": "Could not generate a title.",
                "content": response_data,
                "header_image": None,
                "middle_image": None,
                "additional_content": None
            }

        # Extract images from citations to override/supplement the structured output
        images = []
        if citations:
            images = [c.get('image') for c in citations if c.get('image')]
            print("Images extracted from citations:", len(images))
        
        # Use images from citations if available, otherwise keep from structured output
        header_image = images[0] if len(images) > 0 else article_data.get('header_image')
        middle_image = images[1] if len(images) > 1 else article_data.get('middle_image')

        # Get title from structured output, with fallback from citations
        title = article_data.get('title', 'The New World Times')
        if not title or title == 'The New World Times':
            # Try to get a better title from citations
            for citation in citations:
                if citation.get("title"):
                    title = citation["title"]
                    break

        # Split content if needed for better presentation
        content = article_data.get('content', '')
        additional_content = article_data.get('additional_content')
        
        # If no additional_content was provided in structured output, try to split the main content
        if not additional_content and content:
            # Improved sentence splitting and joining
            sentences = re.split(r'(?<=[.!?])\s+', content)
            sentences = [s.strip() for s in sentences if s.strip()]
            if len(sentences) > 3:  # Only split if we have enough content
                mid_point = len(sentences) // 2
                content = " ".join(sentences[:mid_point])
                additional_content = " ".join(sentences[mid_point:])

        # Construct the final article object
        article = {
            "title": title,
            "headerImage": header_image,
            "content": content,
            "middleImage": middle_image,
            "additionalContent": additional_content
        }
        
        print("Final article structure:", {k: v[:50] + "..." if isinstance(v, str) and len(v) > 50 else v for k, v in article.items()})
        
        return article

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        # Return a default structure on error to avoid frontend issues
        return {
            "title": "Error Generating Article",
            "content": str(e),
            "headerImage": None,
            "middleImage": None,
            "additionalContent": None
        }


app = Flask(__name__)

@app.route('/get-news', methods=['POST'])
def get_news():
    data = request.get_json()

    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400

    prompt = data['prompt']

    try:
        article = generate_article_with_images(prompt)
        return jsonify(article), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)