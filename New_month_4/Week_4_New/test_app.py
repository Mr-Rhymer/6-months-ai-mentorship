import requests

url = "http://127.0.0.1:5000/ai_webhook"
headers = {"X-API-Key": "x7Kp9Qm2Rw5Tz8Vb4Nc6Yf3Gj9Ld1Hs6"}  # same as in .env
payload = {"text": "Python is a programming language used for AI, web development, and automation. It is known for being simple and readable."}

response = requests.post(url, json=payload, headers=headers)
print("Status:", response.status_code)
print("Response:", response.json())