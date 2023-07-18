import requests
import csv

city_dictionary_list = []
base = "https://api.open-meteo.com/v1/forecast?"
extra_link = "&current_weather=true"
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


def weather_code_decipher(code):
    actual_weather = weather_code.get(code)
    return actual_weather


def list_searcher(search_query, list_input):
    matching_dictionaries = []
    search_query = search_query.title()
    for values in list_input:
        if values["city"] == search_query or values["city_ascii"] == search_query:
            matching_dictionaries.append(values)
    return matching_dictionaries


def weather_acquirer(link_base, link_ending, dictionary):
    dictionary_output = dictionary
    if isinstance(dictionary_output, list):
        dictionary_output = dictionary[0]
    latitude = dictionary_output.get('lat')
    longitude = dictionary_output.get('lng')
    path = f"latitude={latitude}&longitude={longitude}"
    api_url = link_base + path + link_ending
    data = requests.get(api_url)
    return data.json()


def format_weather_data(api_input, dictionary):
    dictionary_output = dictionary
    if isinstance(dictionary_output, list):
        dictionary_output = dictionary[0]
    city_name = dictionary_output.get('city')
    country_name = dictionary_output.get('country')
    state_name = dictionary_output.get('admin_name')
    data = api_input
    current_weather = data.get("current_weather")
    temperature = current_weather.get("temperature")
    wind_speed = current_weather.get("windspeed")
    wind_direction = current_weather.get("winddirection")
    actual_weather = weather_code_decipher(current_weather.get("weathercode"))
    print()
    print(f"Latest weather for {city_name}, {state_name}, {country_name}:")
    print("{:^30}|{:^30}".format("Weather", actual_weather))
    print("{:^30}|{:^30}".format("Temperature", f"{temperature}°C"))
    print("{:^30}|{:^30}".format("Wind speed and Direction", f"{wind_speed} km/h, {wind_direction}°"))


with open("worldcities.csv", "r", encoding="UTF-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        city_dictionary_list.append(row)

print("Welcome to the weather searcher.")
user_query = input("What city would you like to know the weather of? ").title()
matching_cities = list_searcher(user_query, city_dictionary_list)
city_found = False
end_search = False
while not city_found:
    if len(matching_cities) == 0:
        print()
        print("There are no cities that match your query.")
        yes_or_no = False
        user_decision = input("Would you like to retry your query? ")
        while not yes_or_no:
            if user_decision.lower() == "yes":
                print()
                yes_or_no = True
                user_query = input("What city would you like to know the weather of? ")
                matching_cities = list_searcher(user_query, city_dictionary_list)
            elif user_decision.lower() == "no":
                print()
                city_found = True
                end_search = True
                yes_or_no = True
            else:
                print()
                print("Input not recognized, please try again.")
                user_decision = input("Would you like to retry your query? ")
    else:
        city_found = True
if end_search:
    print("Have a good day.")
else:
    if len(matching_cities) > 1:
        print()
        print("There is more than one city under your query.")
        print()
        character = 65
        for index, i in enumerate(matching_cities):
            print(f"{chr(character)}. {i['city']}, {i['admin_name']}, {i['country']}")
            character += 1
        print()
        user_choice = input("Which city are you referring to? ").upper()
        real_index = int(ord(user_choice) - 65)
        matching_cities = matching_cities[real_index]

    weather_information = weather_acquirer(base, extra_link, matching_cities)
    format_weather_data(weather_information, matching_cities)