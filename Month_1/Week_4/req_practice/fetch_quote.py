import requests

response = requests.get("https://dummyjson.com/quotes/random")
data = response.json()

print(f"'{data['quote']}'")
print(f"— {data['author']}")