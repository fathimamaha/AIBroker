from flask import Flask, request, jsonify
import utils.llm_utils as llm_utils
from requests import Response
import utils.cache_utils as cache_utils

app = Flask(__name__)
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
    cached_response = cache.get_key(queryid)

    if not cached_response:
        return {}, 202
    
    return cached_response, 200