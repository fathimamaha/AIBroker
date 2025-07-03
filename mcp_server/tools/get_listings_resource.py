from server import mcp
from pathlib import Path
from requests import Response
import requests
import json


# data for mock server
DATA_DIR = Path(__file__).resolve().parent.parent / "data/"
MOCK_LISTING_JSON = "listing_by_id.json"
MOCK_LISTING_JSON = "listings.json"

def mock_listing_details():

    try:
        with open(DATA_DIR+"/listing_by_url.json", 'r') as file:
            data = json.load(file)
            return data

    except FileNotFoundError:
        print(f"Error: The file '{DATA_DIR}' was not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{DATA_DIR}'. Check if the file contains valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return {}

MOCK_DATA = mock_listing_details()

# api info
STREETEASY_API_URL = "https://streeteasy-api.p.rapidapi.com/rentals/"
STREETEASY_API_HEADERS = {
	"x-rapidapi-key": "bb1e10f57bmshc704eaa7632f9d6p1efb95jsn07642b101ab1",
	"x-rapidapi-host": "streeteasy-api.p.rapidapi.com"
}

def fetch_listing_details_by_url(url: str) -> dict:
    """
    Fetch listing details from StreetEasyAPI with the url

    Args:
        url: url of the listing
        
    Returns:
        A dict with listing details
    """

    try:
        query_string = {"url":url}
        response = requests.get(STREETEASY_API_URL+"url", headers=STREETEASY_API_HEADERS, params=query_string)
        listing_details = json.loads(response.json())
        
        #add url to listing details as its not present
        listing_details["listing_url"] = url
    
    except Exception as e:
        print(f"{e} occured while fetching listing details")
        #return mock data
        return MOCK_DATA


@mcp.tool()
def fetch_all_listings_by_params(areas: list[str],
                                 minPrice: float,
                                 maxPrice: float,
                                 minBeds: int,
                                 maxBeds: int,
                                 minBaths: int,
                                 noFee: bool) -> Response:
    """
    Fetch listings from StreetEasyAPI that match the parameters

    Args:
        areas: The NYC areas and neighborhoods to filter for.
        minPrice: The minimum price of a property.
        maxPrice: The maximum price of a property.
        minBeds: The minimum number of bedrooms.
        maxBeds: The maximum number of bedrooms.
        minBaths: The minimum number of bathrooms.
        noFee: Whether to filter for no-fee listings (True or False).

    Example query string:
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
        
    Returns:
        A JSON response with the listings that satisfy the param with their details
    """

    result = []

    try:
        query_string = { "areas" : ','.join(areas),
                        "minPrice": str(minPrice),
                        "maxPrice": str(maxPrice),
                        "minBeds": str(minBeds),
                        "maxBeds": str(maxBeds),
                        "minBaths": str(minBaths),
                        "noFee": str(noFee),
                        "limit":"10",
                        "offset":"0"
        }

        #SCOPE: cache these results so api calls dont have to be made again
        response = requests.get(STREETEASY_API_URL+"search", headers=STREETEASY_API_HEADERS, params=query_string)
        listings_dict = json.loads(response.json())
        for listing in listings_dict["listings"]:
            result.append(fetch_listing_details_by_url(listing["url"]))

    except Exception as e:
        print(f"{e} occured while fetching all listings")

        #if error raised with some results, return current result set
        if result:
            return result
        
        #send mock data
        result.append(MOCK_DATA)
        return result