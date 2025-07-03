#connect to llm and add api utils here

import json
import requests
import threading
from utils.cache_utils import Cache
import anthropic
import uuid

llm_client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-20250514"

LLM_SYSTEM_CONTEXT = f"""You are a helpful NYC real estate assistant. Always respond with a valid JSON only. List out advantages, disadvantages, use emojis, and provide honest insights about listings.

Respond with ONLY valid JSON in this exact format:

{{
  "response": "Your detailed response about the listing with emojis, advantages, and disadvantages",
  "listing_url": "URL to the listing if available, otherwise null",
  "image_url": "First image URL from the listing if available, otherwise null",
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

        message = llm_client.messages.create(
            model=MODEL,
            max_tokens=1000,
            temperature=0.4,
            system=LLM_SYSTEM_CONTEXT,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ]
                }
            ]
        )   

        print(f"Querying LLM with: {message}")

        response_text = message.content[0].text if message.content else ""
        response_data = json.loads(response_text)
            
        if cache and query_id:
            cache.write(query_id, str(response_data))
                
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw response: {message.content}")
    except Exception as e:
        print(f"API call error: {e}")
        cache.write(query_id, str(e)) #REMOE THIS


def start_query(prompt: str, cache: Cache) -> None:
    query_id = str(uuid.uuid4())
    thread = threading.Thread(target=query_and_store, args=(prompt, query_id, cache))
    thread.start()
    return query_id

