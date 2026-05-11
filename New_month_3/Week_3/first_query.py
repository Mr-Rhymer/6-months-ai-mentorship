import sqlite3

conn = sqlite3.connect('chinook.db')
cursor = conn.cursor()
country = input("Enter Country:")
cursor.execute("SELECT  FirstName, LastName, Email FROM customers WHERE Country =?", (country,))
customers = cursor.fetchall()
for customer in customers:
    print(customer)

if not customers:
    print("No customers found in that country.")

conn.close()