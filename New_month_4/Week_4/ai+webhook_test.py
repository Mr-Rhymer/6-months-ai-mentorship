import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("My_API_KEY")

url = "http://127.0.0.1:5000/ai_webhook"
headers = {"X-API-Key": API_KEY}
payload = {"text": "Python is a powerful programming language. It is used for web development, data analysis, AI, and automation. Many companies use Python to build scalable applications."}

response = requests.post(url, json=payload, headers=headers)
print(response.status_code, response.json())