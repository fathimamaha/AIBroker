# AIStreetEasy Backend Server

This is the backend server for the AIStreetEasy project. It acts as an API layer between the web UI and the AI/mcp server, handling user queries and returning NYC rental data.

## How it works

- The UI makes two HTTP requests to this backend:
  1. **POST** `/submit_query`: Accepts a user query and returns a `query_id`.
  2. **GET** `/get_query_response/<query_id>`: The UI polls this endpoint to retrieve the results for the given `query_id`.

- The backend calls the Claude API, using the MCP server as a data source, to fetch and process NYC rental data.

## Running the Server

1. **Set your Anthropic API key** (required for Claude API access):

   ```sh
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```

2. Set the MCP server public https url (refer to the MCP server section on how to expose local host to public):

   ```sh
   export MCP_URL='mcp-server-url'
   ```

3. Start the server using uvicorn:   
   ```sh
   uv run main,py
   ```

The server will be available at http://localhost:9001 by default.

You can install dependencies with:

   ```sh
   pip install .
   ```