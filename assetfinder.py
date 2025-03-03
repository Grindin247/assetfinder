import argparse
import requests
import csv
import os
from typing import List, Tuple

# Get API key from environment variable
API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set")

# Example of how to configure locations
default_locations = [(43232, 10)]  # Can be modified as needed

# Define search parameters
keywords = [
    "non-profit",
    "airport",
    "amusement_park",
    "aquarium",
    "art_gallery",
    "bowling_alley",
    "campground",
    "church",
    "church_of_the_nazarene",
    "city_hall",
    "fire_station",
    "fitness",
    "garden",
    "hospital",
    "library",
    "local_government_office",
    "monument",
    "mosque",
    "movie_theater",
    "museum",
    "night_club",
    "park",
    "police",
    "primary_school",
    "rv_park",
    "school",
    "secondary_school",
    "shelter",
    "stadium",
    "storage",
    "synagogue",
    "thrift_store",
    "tourist_attraction",
    "university",
    "zoo"
]
class Location:
    def __init__(self, zipcode, radius_miles):
        self.zipcode = zipcode
        self.radius_miles = radius_miles

def configure_locations(location_tuples: List[Tuple[str, int]]) -> List[Location]:
    """Convert list of (zipcode, radius) tuples to Location objects"""
    return [Location(zipcode, radius) for zipcode, radius in location_tuples]

# Define the output CSV file
output_file = "sample_assets.csv"

def get_lat_lon(zipcode):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zipcode}&key={API_KEY}"
    response = requests.get(url).json()
    if "results" in response and response["results"]:
        location = response["results"][0]["geometry"]["location"]
        return f"{location['lat']},{location['lng']}"
    return None
    
# Function to search places using Google Places API
def search_places(keyword, location, radius):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": API_KEY,
        "location": location,
        "radius": radius,
        "keyword": keyword
    }
    response = requests.get(url, params=params)
    return response.json()

def parse_location(location_str: str) -> Tuple[int, int]:
    """Parse location string in format 'zipcode:radius'"""
    try:
        zipcode, radius = location_str.split(':')
        return (int(zipcode), int(radius))
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Location must be in format 'zipcode:radius' (e.g., '43232:10')"
        )

def parse_args():
    parser = argparse.ArgumentParser(
        description='Find assets near specified locations using Google Places API'
    )
    parser.add_argument(
        '-l', '--locations',
        type=parse_location,
        nargs='+',
        default=[(43232, 10)],
        help='Locations in format "zipcode:radius" (e.g., "43232:10"). Can specify multiple.'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='sample_assets.csv',
        help='Output CSV file path (default: sample_assets.csv)'
    )
    return parser.parse_args()

# Rest of the code remains the same until main()...

def main():
    args = parse_args()
    locations = configure_locations(args.locations)
    
    unique_entries = set()
    with open(args.output, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Category", "Address", "Description"])
        
        for location in locations:
            zipcode = location.zipcode
            radius_miles = location.radius_miles
            location_coords = get_lat_lon(zipcode)
            if not location_coords:
                raise ValueError(f"Invalid ZIP code or unable to fetch coordinates for {zipcode}")
            radius = radius_miles * 1609.34  # Convert miles to meters
            
            for keyword in keywords:
                data = search_places(keyword, location_coords, radius)
                
                if "results" in data:
                    for place in data["results"]:
                        name = place.get("name", "N/A")
                        category = keyword
                        address = place.get("vicinity", "N/A")
                        description = place.get("types", [])
                        description = ", ".join(description) if description else "N/A"
                        
                        entry = (name, category, address, description)
                        if entry not in unique_entries:
                            unique_entries.add(entry)
                            writer.writerow(entry)

    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main()