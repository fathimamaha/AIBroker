# AIStreetEasy MCP Server

This is the MCP (Multi-Component Pipeline) server for the AIStreetEasy project. It provides tools for querying NYC rental listings from the RedAPI StreetEasy API (https://rapidapi.com/realestator/api/streeteasy-api/playground/apiendpoint_9e37dc9d-f9dd-4601-8447-21cc9717db0c) and serves as a data source for the AI backend. If the API fails for some reason, there is a mock data that we return that mocks the API call.

## MCP Tool: fetch_all_listings_by_params

This tool fetches rental listings from the RedAPI StreetEasy API that match the provided parameters.

### Arguments

- **areas**: The NYC areas and neighborhoods to filter for.
- **minPrice**: The minimum price of a property.
- **maxPrice**: The maximum price of a property.
- **minBeds**: The minimum number of bedrooms.
- **maxBeds**: The maximum number of bedrooms.
- **minBaths**: The minimum number of bathrooms.
- **noFee**: Whether to filter for no-fee listings (`True` or `False`).

#### Example query string

```json
{
    "areas": "all-downtown,all-midtown",
    "minPrice": "2000",
    "maxPrice": "4000",
    "minBeds": "1",
    "maxBeds": "10",
    "minBaths": "1",
    "noFee": "false",
    "limit": "100",
    "offset": "0"
}
```

## Running the Server

1. Export your StreetEasy API key (required):

   ```sh
   export STREETEASY_API_KEY='your-rapidapi-key-here'
   ```

2. Start the MCP server (runs on port 9000):

   ```sh
   uv run main.py
   ```

3. Expose the MCP server to the public (required for Claude/AI backend to access). The MCP server must be accessible via a public HTTPS URL. For development, you can use ngrok (Warning: Exposing your local server to the public internet can be risky. For production, host the MCP server securely on a cloud provider.):  

   ```sh
   ngrok http 9000
   ```

4. Set the MCP server public HTTPS URL (for the backend to connect):   

   ```sh
   export MCP_URL='<mcp-server-url>/mcp/'
   ```



You can install dependencies with:

   ```sh
   pip install .
   ```