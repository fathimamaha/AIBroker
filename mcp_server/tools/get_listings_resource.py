from server import mcp
from pathlib import Path
from requests import Response
import json


# Base directory where our data lives
DATA_DIR = Path(__file__).resolve().parent.parent / "data/listing_by_id.json"

def fetch_listing_details_by_id(id: str) -> dict:

    try:
        with open(DATA_DIR, 'r') as file:
            data = json.load(file)
            return data

    except FileNotFoundError:
        print(f"Error: The file '{DATA_DIR}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{DATA_DIR}'. Check if the file contains valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return


@mcp.tool()
def fetch_all_listings_by_params(areas: list[str]) -> Response:
    """
    Fetch listings from StreetEasyAPI that match the parameters

    Args:
        areas: The NYC areas and neighborhoods to filter for.
        minPrice: The minimum price of a property
        maxPrice: The maximum price of a property
        
    Returns:
        A JSON response with the listings that satisfy the param
    """
    
    mock = True

    if mock:
        return fetch_listing_details_by_id("foo"), 200
    else:

        #make the api call

        #get listings
        #cache the query in redis? yes cuz i only have so many api calls?

        #iterate through listing and call fetch listing by id, return the details, for each listing as a list,
        # llm will take care of choosing one

        #when my ui sends the query to llm api it should tell, return the best listing, list out advantages and disavanatges with emojis
        #and if you have url provide it to me as a response { content, one image url, lisitng url}


        return
