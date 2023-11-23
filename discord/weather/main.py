import requests
import csv
from pathlib import Path

def weather_code_decipher(code):
    weather_code = {0: "Clear sky",
                    1: "Mainly Clear",
                    2: "Partly Cloudy",
                    3: "Overcast",
                    45: "Fog",
                    48: "Depositing Rime Fog",
                    51: "Light Drizzle",
                    53: "Moderate Drizzle",
                    55: "Dense Drizzle",
                    56: "Light Freezing Drizzle",
                    57: "Dense Freezing Drizzle",
                    61: "Slight Rain",
                    63: "Moderate Rain",
                    65: "Heavy Rain",
                    66: "Light Freezing Rain",
                    67: "Heavy Freezing Rain",
                    71: "Slight Snowfall",
                    73: "Moderate Snowfall",
                    75: "Heavy Snowfall",
                    77: "Snow Grains",
                    80: "Slight Showers",
                    81: "Moderate Showers",
                    82: "Violent Showers",
                    85: "Slight Snow",
                    86: "Heavy Snow",
                    95: "Thunderstorm",
                    96: "Slight Hail Thunderstorm",
                    99: "Heavy Hail Thunderstorm"}
    actual_weather = weather_code.get(code)
    return actual_weather

filepath = Path(__file__).parent / "worldcities.csv"

def list_searcher(search_query):
    city_dictionary_list = []
    with open(filepath, "r", encoding="UTF-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            city_dictionary_list.append(row)
    matching_dictionaries = []
    search_query = search_query.title()
    for values in city_dictionary_list:
        if values["city"] == search_query or values["city_ascii"] == search_query:
            matching_dictionaries.append(values)
    return matching_dictionaries


def weather_acquirer(dictionary):
    link_base = "https://api.open-meteo.com/v1/forecast?"
    link_ending = "&current_weather=true&timezone=Australia%2FSydney"
    dictionary_output = dictionary
    if isinstance(dictionary_output, list):
        dictionary_output = dictionary[0]
    latitude = dictionary_output.get('lat')
    longitude = dictionary_output.get('lng')
    path = f"latitude={latitude}&longitude={longitude}"
    api_url = link_base + path + link_ending
    data = requests.get(api_url)
    return data.json()