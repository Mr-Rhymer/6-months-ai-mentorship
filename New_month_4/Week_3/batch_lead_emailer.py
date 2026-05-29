import os
import time 
import csv
from dotenv import load_dotenv
from groq import Groq
from serper_test import search_company
import logging
import sqlite3


conn = sqlite3.connect('leads_emails.db')
cursor = conn.cursor()


logging.basicConfig(filename = 'lead_emailer.log',
                   level = logging.INFO,
                   format = '%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

client = Groq(api_key=groq_api_key)

def serper_with_retry(company_name, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = search_company(company_name)
            return result
        except Exception as e:
            logging.error(f"Serper attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

def call_groq_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Groq attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

def work_with_leads():
    emails = {}  
    success = 0
    failed = 0
    with open("leads.csv", "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        for idx, row in enumerate(rows, 1):
            company_name = row['company']   
            logging.info(f"Processing {idx}/{len(rows)}: {company_name}")
            try:
                info = serper_with_retry(company_name)
                description = info['description']
                if description and description != "No description found." and description != "No search results found.":
                    prompt = f"""Write a short professional email to {company_name} with the description: {description} to offer a free AI consultation."""
                else:
                    prompt = f"""Write a short professional email to {company_name} to offer a free AI consultation."""
                reply = call_groq_with_retry(prompt)
                emails[company_name] = reply
                logging.info(f"Successfully generated email for {company_name}")
                success += 1
            except Exception as e:
                logging.error(f"Failed to generate email for {company_name}: {e}")
                failed += 1
    logging.info(f"Batch completed: {success} succeeded, {failed} failed")
    return emails


def save_emails_to_file(emails):
    try:
        with open("generated_emails.txt", "w") as f:
            for i, (company, email) in enumerate(emails.items(), 1):
                f.write(f"--- Email for {company} ---\n{email}\n\n")
        logging.info(f"Saved {len(emails)} emails to generated_emails.txt")
    except Exception as e:
        logging.error(f"Error saving emails: {e}")

def save_to_db(emails):
    try:
        cursor.execute(
        '''CREATE TABLE IF NOT EXISTS lead_emails (email_id INTEGER PRIMARY KEY AUTOINCREMENT,
          company_name TEXT NOT NULL, email_content TEXT NOT NULL,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);''')
        for company, email in emails.items():
            cursor.execute('''INSERT INTO lead_emails (company_name, email_content) VALUES (?, ?)''', (company, email))
        conn.commit()
    except Exception as e:
        logging.error(f"Error creating database table: {e}")
        return None

def main():
    emails = work_with_leads()
    if emails:
        save_emails_to_file(emails)
        save_to_db(emails)



    
if __name__ == "__main__":
    main()