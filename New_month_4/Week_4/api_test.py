import requests

url = "http://127.0.0.1:5000/secure_webhook"
headers = {"X-API-Key": "kX9mP2qR5sT8vW1yZ4aB7cD0eF3gH6jL"}
payload = {"test": "data"}

response = requests.post(url, json=payload, headers=headers)
print("Status Code:", response.status_code)
print("Response Text:", response.text)

if response.headers.get("Content-Type", "").startswith("application/json"):
    print("Response JSON:", response.json())
else:
        print("Response is not JSON.")   