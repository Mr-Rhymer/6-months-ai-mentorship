import requests
import sys

if len(sys.argv) > 1:
    city_name = sys.argv[1]          # take first argument
else:
    city_name = input("Enter the city name: ")
 
geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
geocode_params = {"name": city_name}

# Retry up to 3 times, with user choice
max_retries = 3
geo_data = None

for attempt in range(1, max_retries + 1):
    try:
        geo_response = requests.get(geocode_url, params=geocode_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        break  # success – exit loop
    except Exception as e:
        print(f"Attempt {attempt} failed: {e}")
        if attempt == max_retries:
            print("Max retries reached. Exiting.")
            exit(1)
        retry = input("Retry? (y/n): ").lower()
        if retry != 'y':
            exit(1)
        # otherwise, continue to next attempt

# Now we have geo_data
if not geo_data or not geo_data.get("results"):
    print(f"City '{city_name}' not found.")
    exit(1)

results = geo_data["results"]
if len(results) > 1:
    print("Multiple cities found:")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['name']}, {r.get('country', 'Unknown')}")
    try:
        choice = int(input("Select a number: ")) - 1
        selected = results[choice]
    except (ValueError, IndexError):
        print("Invalid choice.")
        exit(1)
else:
    selected = results[0]

lat = selected["latitude"]
lon = selected["longitude"]
official_name = selected["name"]
country = selected.get("country", "")

# Fetch weather (you can also add retry here if desired)
weather_url = "https://api.open-meteo.com/v1/forecast"
weather_params = {
    "latitude": lat,
    "longitude": lon,
    "current_weather": True
}

try:
    weather_response = requests.get(weather_url, params=weather_params)
    weather_response.raise_for_status()
    weather_data = weather_response.json()
except Exception as e:
    print(f"Error fetching weather: {e}")
    exit(1)

# Display results
current = weather_data["current_weather"]
print(f"\nWeather in {official_name}, {country}:")
print(f"Temperature: {current['temperature']}°C")
print(f"Wind Speed: {current['windspeed']} km/h")
print(f"Wind Direction: {current['winddirection']}°") 


save = input("\nSave report to file? (y/n): ").lower()
if save == 'y':
    report = f"Weather in {official_name}, {country}:\n"
    report += f"Temperature: {current['temperature']}°C\n"
    report += f"Wind Speed: {current['windspeed']} km/h\n"
    report += f"Wind Direction: {current['winddirection']}°\n"
    with open("weather_report.txt", "w") as f:
        f.write(report)
    print("Report saved to weather_report.txt")