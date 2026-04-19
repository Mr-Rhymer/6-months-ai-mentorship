import requests
import json
import csv
from groq import Groq
from dotenv import load_dotenv
import os
import time

load_dotenv()
serper_api_key = os.getenv("Serper_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

def search_company_info(company_name):
    """
    Searches for a company using Serper API and returns the first organic result's snippet.
    """
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": company_name})
    headers = {
        'X-API-KEY': serper_api_key,  # Use the API key from your .env
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        # Try to get the first organic result's snippet
        if data.get('organic') and len(data['organic']) > 0:
            return data['organic'][0].get('snippet', 'No description found.')
        else:
            return "No search results found."

    except requests.exceptions.RequestException as e:
        print(f"Error calling Serper API: {e}")
        return "Could not retrieve company information."
    

# Initialize your Groq client
client = Groq(api_key=groq_api_key)
def call_api_with_retry(client, prompt, max_retries=3):
                    for attempt in range(max_retries):
                       try:
                         response = client.chat.completions.create(
                         model="llama-3.3-70b-versatile",
                         messages=[{"role": "user", "content": prompt}])
                         return response.choices[0].message.content
                       except Exception as e:
                           print(f"Attempt {attempt+1} failed: {e}")
                           if attempt == max_retries - 1:
                            raise  # re-raise the error after last attempt
                           wait_time = 2 ** attempt  # 1 second, then 2, then 4
                           print(f"Waiting {wait_time} seconds before retry...")
                           time.sleep(wait_time)
# Open your output file
with open("enriched_emails.txt", "w") as outfile:
    # Open and read your leads CSV
    with open("leads.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # 1. Get the company info from Serper
            company_info = search_company_info(row['company'])
            
            # 2. Build your prompt for Groq, including the new search data
            prompt = f"""Write a short, professional email to {row['name']} at {row['company']} ({row['industry']}).
Here is some recent information I found about the company: {company_info}
The email should offer a free 15-minute consultation about AI automation.
Keep it under 100 words."""
            
            # 3. Call Groq to generate the email (using your retry logic)
            try:
                # This uses the call_api_with_retry function you created earlier
                email = call_api_with_retry(client, prompt)
                
                # Write the email to the file
                outfile.write(f"--- Email for {row['name']} ---\n{email}\n\n")
                print(f"Generated email for {row['name']}...")
            except Exception as e:
                print(f"Failed to generate email for {row['name']}: {e}")
                outfile.write(f"--- Email for {row['name']} ---\nERROR: {e}\n\n")