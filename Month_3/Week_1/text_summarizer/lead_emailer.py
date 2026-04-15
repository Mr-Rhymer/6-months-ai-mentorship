from groq import Groq
from dotenv import load_dotenv
import os
import csv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Open output file for writing
with open("personalized_emails.txt", "w") as outfile:
    # Read leads.csv
    with open("leads.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Build prompt using row['name'], row['company'], etc.
            # Call Groq
            # Write to outfile with separator
            # Print to console
            prompt = f"""Write a short, professional email to {row['name']} at {row['company']} ({row['industry']}).
Mention this note: {row['notes']}.
The email should offer a free 15-minute consultation about AI automation.
Keep it under 100 words."""
            try:
                response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}])
                email = response.choices[0].message.content
                outfile.write(f"--- Email for {row['name']} ---\n{email}\n\n")
                print(f"Generated email for {row['name']}:\n{email}\n")
            except Exception as e:
              print(f"Error generating email reply: {e}")
           