# Asset Finder

A Python script that uses the Google Places API to find various points of interest and assets near specified locations.

## Description

Asset Finder searches for various establishments and points of interest (like schools, parks, churches, etc.) within a specified radius of given ZIP codes. It uses the Google Maps and Places APIs to gather this information and outputs the results to a CSV file.

## Prerequisites

- Python 3.6+
- Google Maps API key
- Required Python packages:
  - requests
  - typing

## Installation

1. Clone this repository
2. Install required packages:
```bash
pip install requests
```
3. Set your Google Maps API key as an environment variable:
```bash
export GOOGLE_MAPS_API_KEY='your-api-key-here'
```

## Usage

Basic usage with default location (ZIP code 43232, 10-mile radius):
```bash
python assetfinder.py
```

Specify custom locations and radius:
```bash
python assetfinder.py -l 43232:10 90210:5
```

Specify custom output file:
```bash
python assetfinder.py -o my_assets.csv
```

### Command Line Arguments

- `-l, --locations`: Locations in format "zipcode:radius" (e.g., "43232:10"). Can specify multiple.
- `-o, --output`: Output CSV file path (default: sample_assets.csv)

## Output

The script generates a CSV file with the following columns:
- Name: Name of the establishment
- Category: Type of establishment (based on search keywords)
- Address: Physical address
- Description: Additional details about the establishment

## Search Categories

The script searches for various types of establishments including:
- Non-profits
- Airports
- Amusement parks
- Churches
- Schools
- Museums
- Parks
- And many more...