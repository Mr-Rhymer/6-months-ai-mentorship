import requests
import json

url =  url = "http://127.0.0.1:5000/webhook"
payload = {"name": "Zhun", "company": "XiaoMi", "industry": "Tech"}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
    