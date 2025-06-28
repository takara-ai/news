from pydantic import BaseModel, Field
from openai import OpenAI

client = OpenAI()



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

    completion = client.chat.completions.parse(
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