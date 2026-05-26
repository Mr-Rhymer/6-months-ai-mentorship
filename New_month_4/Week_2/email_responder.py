import csv
import datetime as dt
from groq import Groq
from dotenv import load_dotenv
import os
import time
import sqlite3
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
try:
    conn = sqlite3.connect('responses.db')
    cursor = conn.cursor()
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit(1)

def generate_reply(email_content, tone, client, max_retries=3):
    prompt = f"""You are an AI email assistant. Write a {tone} reply to the email below.
    Output a valid JSON object with two fields: "reply" (the email text) and "confidence" (an integer from 1 to 10).
    Do not include any other text.

    Email: {email_content}
    """
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            raw = response.choices[0].message.content
            # Try to parse JSON
            data = json.loads(raw)
            return data["reply"], data["confidence"]
        except json.JSONDecodeError:
            # If JSON parsing fails, fallback: treat raw text as reply, confidence None
            return raw, None
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

def init_db():         
            try:
                 cursor.execute(
        '''CREATE TABLE IF NOT EXISTS responses (
    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_content TEXT NOT NULL,
    tone TEXT NOT NULL,
    reply TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);''')
                 conn.commit()
            except Exception as e:
                print(f"Error initializing database: {e}")
                return None

def add_confidence_score():
    try:
        cursor.execute("ALTER TABLE responses ADD COLUMN confidence_score INTEGER")
        conn.commit()
    except sqlite3.OperationalError as e:
        if "duplicate column name" not in str(e):
            raise
    try: 
         cursor.execute("SELECT response_id, reply FROM responses")
         rows = cursor.fetchall()
         for row in rows:
                response_id, reply = row
                if "Confidence score:" in reply:
                    parts = reply.split("Confidence score:")
                    reply_text = parts[0].strip()
                    confidence = int(parts[1].strip())
                    cursor.execute("UPDATE responses SET confidence_score = ?, reply = ? WHERE response_id = ?", (confidence, reply_text, response_id))
                conn.commit()
    except Exception as e:
        print(f"Error adding confidence scores: {e}")

    return None 
         
def export_replies_to_csv():
    try:
        cursor.execute("SELECT * FROM responses")
        rows = cursor.fetchall()
        with open(f'responses_{dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Email Content', 'Tone', 'Reply', 'Timestamp', 'Confidence Score'])
            writer.writerows(rows)
        print("Replies exported to responses.csv")
    except Exception as e:
        print(f"Error exporting replies to CSV: {e}")

if __name__ == "__main__":
    try:
        init_db() 
        add_confidence_score()  
        email_content = input("Enter the content of the email you want to reply to: ")
        tone = input("Enter the desired tone for the reply (e.g., formal, casual, informative, emphatic, urgent ): ")
    
        reply_text, confidence = generate_reply(email_content, tone, client)
        print(f"Generated Reply: \n{reply_text}")
        cursor.execute(
            "INSERT INTO responses (email_content, tone, reply, confidence_score) VALUES (?, ?, ?, ?)",
            (email_content, tone, reply_text, confidence)
        )
        conn.commit()
        print("Response saved to database.")
        print("Do you want to view all past responses? (yes/no)")
        ans = input().lower()
        if ans == "yes" or ans == "y":
            cursor.execute("SELECT * FROM responses")
            responses = cursor.fetchall()
            for response in responses:
                print(f'''ID: {response[0]} | Email Content: {response[1]} | Tone: {response[2]} | Reply: {response[3]} | Timestamp: {response[4]} | Confidence Score: {response[5]}''')
        print("Do you want to export all responses to a CSV file? (yes/no)")
        export_ans = input().lower()       
        if export_ans == "yes" or export_ans == "y":
            export_replies_to_csv()
        else:
            print("Exiting without exporting.")
    except Exception as e:
        print(f"Failed to generate email reply: {e}")
    conn.close()