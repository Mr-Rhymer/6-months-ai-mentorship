import requests
import time

def fetch_joke_with_retry(max_retries=3):
    url = "https://api.chucknorris.io/jokes/random"
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data['value']
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

if __name__ == "__main__":
    joke = fetch_joke_with_retry()
    print(joke)