import sqlite3 
import json
import csv


try:
    conn = sqlite3.connect('titanic.db')
    cursor = conn.cursor()
except Exception as e:
    print(f"An error occurred while connecting to the database: {e}")

def export_to_json():
    try:
        cursor.execute("SELECT * FROM passengers")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        with open('titanic_cleaned.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print("Data exported to titanic_cleaned.json")
    except Exception as e:
        print(f"An error occurred while exporting to JSON: {e}")

def export_to_csv():
    try:
        cursor.execute("SELECT * FROM passengers")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        with open('titanic_cleaned.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(columns)
            writer.writerows(rows)
        print("Data exported to titanic_cleaned.csv")
    except Exception as e:
        print(f"An error occurred while exporting to CSV: {e}")


try:
    export_to_json()
    export_to_csv()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()