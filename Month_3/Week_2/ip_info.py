import time
import requests

url = "https://ipapi.co/json/"
def get_ip_info(max_retries=3):
    for tries in  range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data =response.json()
            return data['ip'], data['city'], data['country_name']
        except Exception as e:
            print(f"Attempt {tries+1} failed: {e}")
            if tries == max_retries - 1:
                raise
            time.sleep(2 ** tries)

if __name__ == "__main__":
    ip_info = get_ip_info()
    print(ip_info)