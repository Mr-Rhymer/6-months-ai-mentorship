import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 6.6666,   # approximate for Kumasi, Ghana
    "longitude": -1.6163,
    "current_weather": True
}

response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    print("Weather data received:")
    print(data["current_weather"]["temperature"])
else:
    print(f"Error: {response.status_code}")