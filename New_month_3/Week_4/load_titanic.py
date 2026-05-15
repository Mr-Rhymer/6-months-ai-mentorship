import sqlite3
import csv

try:
    conn = sqlite3.connect('titanic.db')
    cursor = conn.cursor()
except Exception as e:
    print("Error connecting to database:", e)

def init_db():
    try:
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS passengers (
                passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
                survived INTEGER,
                pclass INTEGER,
                name TEXT,
                sex TEXT,
                age REAL,
                sibsp INTEGER,
                parch INTEGER,
                ticket TEXT,
                fare REAL,
                cabin TEXT,
                embarked TEXT
            )'''
        )
        conn.commit()
    except Exception as e:
        print("Error initializing database:", e)

def load_data_from_csv():
    try:
        with open('titanic.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                survived = int(row['Survived']) if row['Survived'] else None
                pclass = int(row['Pclass']) if row['Pclass'] else None
                age = float(row['Age']) if row['Age'] else None
                sibsp = int(row['SibSp']) if row['SibSp'] else None
                parch = int(row['Parch']) if row['Parch'] else None
                fare = float(row['Fare']) if row['Fare'] else None
                # Cabin and Embarked: empty string becomes None
                cabin = row['Cabin'] if row['Cabin'] else None
                embarked = row['Embarked'] if row['Embarked'] else None
                cursor.execute(
                    '''INSERT INTO passengers (survived, pclass, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (survived, pclass, row['Name'], row['Sex'], age, sibsp, parch, row['Ticket'], fare, cabin, embarked))
            conn.commit()
            print("Data loaded successfully.")  
    except Exception as e:
        print("Error loading data from CSV:", e)

    
if __name__ == "__main__":
    init_db()
    load_data_from_csv()