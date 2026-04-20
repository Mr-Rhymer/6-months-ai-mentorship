import requests
import time

def get_weather(max_retries=3):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 6.6666,   # approximate for Kumasi, Ghana
        "longitude": -1.6163,
        "current_weather": True
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data["current_weather"]["temperature"]
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)