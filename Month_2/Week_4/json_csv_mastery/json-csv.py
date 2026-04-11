import json
import csv

data = None  # initialize

try:
    with open('inventory.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    print("File not found.")
    exit(1)  # stop execution

# Only proceed if data was loaded
if data and isinstance(data, list) and len(data) > 0:
    try:
        with open('inventory1.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print("CSV written successfully.")
    except Exception as e:
        print(f"An error occurred while writing CSV: {e}")
else:
    print("No valid data to write.")