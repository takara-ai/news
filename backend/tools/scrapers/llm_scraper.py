import os
from dotenv import load_dotenv
from .prompts import EXTRACT_PROMPT
import re
from openai import OpenAI

load_dotenv()

base_url = os.environ.get("OPENAI_URL")
api_key = os.environ.get("OPENAI_TOKEN")
extraction_model = os.environ.get("OPENAI_MODEL")

print(f"INFO: Using model {extraction_model}")

if not base_url or not api_key or not extraction_model:
    raise ValueError("Environment variables OPENAI_URL, OPENAI_TOKEN, and OPENAI_MODEL must be set.")

client = OpenAI(
    base_url=base_url,
    api_key=api_key
)

def completion(messages: list) -> dict:
    result = client.chat.completions.create(
        model=extraction_model,
        messages=messages,
        temperature=0.25,
        max_tokens=1024*8
    )
    return result.choices[0].message

def extract(text: str) -> str:
    messages = [
        {"role": "system", "content": EXTRACT_PROMPT},
        {"role": "user", "content": text},
    ]
    result = completion(messages)
    content = result.content
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL) # CoT is stupid like this
    return content.strip()


# for later i guess if we have time

"""
def bias_to_number(bias: str) -> int:
    bias_map = {
        "left": -2,
        "slightly left": -1,
        "neutral": 0,
        "slightly right": 1,
        "right": 2,
    }
    return bias_map.get(bias, 0)

def bias(text: str) -> str:
    messages = [
        {"role": "system", "content": BIAS_PROMPT},
        {"role": "user", "content": text},
    ]
    result = completion(messages)
    content = result.content.lower()
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
    return bias_to_number(content.strip())
"""