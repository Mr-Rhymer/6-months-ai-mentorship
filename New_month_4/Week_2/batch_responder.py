from email_responder import generate_reply,init_db
from groq import Groq
from dotenv import load_dotenv
import os
import time
import sqlite3
import csv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    conn = sqlite3.connect('responses.db')
    cursor = conn.cursor()
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit(1)

init_db()
total = 0
success = 0
failed = 0
with open('emails.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)
    total = len(rows)
    
    for idx, row in enumerate(rows,1):
        email_content = row['email_content']
        tone = row['tone']
        try:
            reply = generate_reply(email_content, tone, client)
            print(f"Processed {idx}/{total}: Success")
            success += 1
             
            cursor.execute(
                "INSERT INTO responses (email_content, tone, reply) VALUES (?, ?, ?)",
                (email_content, tone, reply)
            )
            conn.commit()
        except Exception as e:
            print(f"Error processing email: {e}")
            failed += 1
    
conn.close()    
print(f"Batch completed: {success} succeeded, {failed} failed")
print(f"Do you want to view the generated replies? (yes/no)")
view_replies = input().lower()
if view_replies == "yes" or view_replies == "y":
    cursor.execute("SELECT * FROM responses")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Email: {row[0]}\nTone: {row[1]}\nReply: {row[2]}\n")
else:    print("Exiting without displaying replies.")
conn.close()