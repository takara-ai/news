from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()

client = OpenAI(
    base_url=os.environ.get("OPENAI_URL"),
    api_key=os.environ.get("OPENAI_API_KEY")
)

class NewsArticle(BaseModel):
    title: str = Field(
        description="The title or headline of the news article."
    )
    paragraph: str = Field(
        description="The main content or body of the news article."
    )


def generate_news_schema(content:str):
    NEWS_SCHEMA_SYS="""Give an Unstructured News parsed for various sources your role is to structure the news article in proper format:" 
    Here is the unstrcutured content {content}"""

    completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": NEWS_SCHEMA_SYS},
            {"role": "user", "content": content}

        ],
        response_format=NewsArticle,
    )
    

    math_reasoning = completion.choices[0].message
    answer=math_reasoning.to_json()
    return answer




NEWS_WEB_SEARCH_SYS="""I have created a news website where user will provide some input regarding the topic they wnated to get the news on,

and I will provide them with the detail news artcile to read on realted to that topic by doing the websearch and find all the recent things happens related to the give topic. Your role here is to 
help me in preparing the news artciles by doing the webserch and collect information from the web. Once you collect the information draft it into an artcile format which I will directly display on my UI. 
"""
def oai_websearch(query: str, provider='oai'):
    if provider=='oai':
        completion = client.chat.completions.create(
            model="gpt-4o-search-preview",
            messages=[
                    {"role": "system", "content": NEWS_WEB_SEARCH_SYS},
                    {"role": "user", "content": query}

                ],
        )
        return completion.choices[0].message.content


  
    if provider=='google':
    # Configure the client
        client = genai.Client()

        # Define the grounding tool
        grounding_tool = types.Tool(
            google_search=types.GoogleSearch()
        )

        # Configure generation settings
        config = types.GenerateContentConfig(
            tools=[grounding_tool]
        )

        # Make the request
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=NEWS_WEB_SEARCH_SYS+'Here the user query:'+query,
            config=config,
        )
        return response.text


        # Print the grounded response
        #print(response.text)



