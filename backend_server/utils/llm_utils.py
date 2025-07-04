import json
import threading
from utils.cache_utils import Cache
import anthropic
import uuid
import os

llm_client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-20250514"
MCP_URL = os.environ.get("MCP_URL")

LLM_SYSTEM_CONTEXT = f"""You are a helpful NYC real estate assistant. Always respond with a valid JSON only. List out advantages, disadvantages, use emojis, and provide honest insights about listings.

Respond with ONLY valid JSON in this exact format, strictly start the JSON with curly brace and end with curly brace. Keep in mind any result you return even if it is not about the listing add to it to the content field of the json:

{{
  "content": "Your detailed response text about the listing with emojis, advantages, and disadvantages, format this response content it as an html",
  "url": "URL to the listing if available, otherwise null, format as a string",
  "image": "First image URL from the listing if available, otherwise null, format it as a string",
}}

Requirements:
- Include emojis in your response 🏠
- List at least 3 advantages and 3 disadvantages
- Be honest about pros and cons
- Respond with JSON only, no other text"""


def query_and_store(user_prompt: str, query_id: str, cache: Cache) -> None:
    """
    Query LLM API to get structured listing data
    """
    
    try:

        message = llm_client.beta.messages.create(
            model=MODEL,
            max_tokens=1000,
            temperature=0.4,
            system=LLM_SYSTEM_CONTEXT,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            mcp_servers=[{
                "type": "url",
                "url": MCP_URL+"/mcp/",
                "name": "aibroker-mcp"            
            }],
            extra_headers={
                "anthropic-beta": "mcp-client-2025-04-04"
            }
        )   

        #fetch the last response from mcp as there are multiple result options returned
        response_text = message.content[-1].text if message.content else ""
        response_data = json.loads(response_text)
        print(f"Raw response: {message.content}")

        if "content" not in response_data or response_data["content"] == None:
            response_data["content"] = str(response_text)

        if "url" not in response_data or response_data["url"] == None:
            response_data["url"] = "https://streeteasy.com/"
            
        if "image" not in response_data or response_data["image"] == None:
            response_data["image"] = "https://miro.medium.com/v2/resize:fit:1069/1*caByH6RLCHxfGvDewB7Faw.jpeg"

        if cache and query_id:
            cache.write(query_id, json.dumps(response_data))
                
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {message.content}")
    except Exception as e:
        print(f"API call error: {e}")

def start_query(prompt: str, cache: Cache) -> None:
    query_id = str(uuid.uuid4())
    thread = threading.Thread(target=query_and_store, args=(prompt, query_id, cache))
    thread.start()
    return query_id

