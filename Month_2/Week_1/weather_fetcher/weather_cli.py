import requests

city_name = input("Enter the city name: ")

# 1. Geocoding: get coordinates
geocode_url = f"https://geocoding-api.open-meteo.com/v1/search"
geocode_params = {"name": city_name}

try:
    geo_response = requests.get(geocode_url, params=geocode_params)
    geo_data = geo_response.json()
except Exception as e:
    print(f"Network error while geocoding: {e}")
    exit(1)

# Check if city was found
if not geo_data.get("results"):
    print(f"City '{city_name}' not found.")
    exit(1)

# Extract first result
first_result = geo_data["results"][0]
lat = first_result["latitude"]
lon = first_result["longitude"]
official_name = first_result["name"]
country = first_result.get("country", "")

# 2. Fetch weather
weather_url = "https://api.open-meteo.com/v1/forecast"
weather_params = {
    "latitude": lat,
    "longitude": lon,
    "current_weather": True
}

try:
    weather_response = requests.get(weather_url, params=weather_params)
    weather_response.raise_for_status()  # Raises an error for bad status codes
    weather_data = weather_response.json()
except Exception as e:
    print(f"Error fetching weather: {e}")
    exit(1)

# 3. Display results
current = weather_data["current_weather"]
print(f"\nWeather in {official_name}, {country}:")
print(f"Temperature: {current['temperature']}°C")
print(f"Wind Speed: {current['windspeed']} km/h")
print(f"Wind Direction: {current['winddirection']}°")