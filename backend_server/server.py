from flask import Flask, request, jsonify
import utils.llm_utils as llm_utils
from requests import Response
import utils.cache_utils as cache_utils
import json
from flask_cors import CORS #can remove this

app = Flask(__name__)
CORS(app)
cache = cache_utils.Cache()

@app.route("/")
def health():
    return "Backend Server is running!"

@app.route("/submit_query", methods=["POST"])
def submit_prompt() -> Response:
    data = request.get_json()


    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing 'prompt' in request body"}), 400

    prompt = data['prompt']
    
    query_id = llm_utils.start_query(prompt, cache)
    return jsonify({"query_id": query_id}), 200

@app.route("/get_query_response/<queryid>", methods=["GET"])
def get_query_response(queryid: str) -> Response:
    print(cache.storage)
    cached_response = cache.get_key(queryid)

    if not cached_response:
        return {}, 202

    cached_response = {"content": cached_response, "image" : "https://miro.medium.com/v2/resize:fit:1069/1*caByH6RLCHxfGvDewB7Faw.jpeg", "url" : "https://streeteasy.com/"}
    json_cached_response = {}
    print(cached_response)

    #for any nonsense repsonse send a cute image and some url funny

    try:
        json_cached_response = json.dumps(cached_response)
    except (ValueError, TypeError) as e:
        print(e)
        return {}, 202

    return json_cached_response, 200