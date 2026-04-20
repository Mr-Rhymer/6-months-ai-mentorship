import requests
import json
import csv
from groq import Groq
from dotenv import load_dotenv
import os
import time
from tqdm import tqdm
import logging


with open("config.json", "r") as f:
    config = json.load(f)

logging.basicConfig(
    filename=config["log_file"],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
CHECKPOINT_FILE = config["checkpoint_file"]

def load_checkpoint():
    try:
        with open(CHECKPOINT_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_checkpoint(lead_name):
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(lead_name)


load_dotenv()
serper_api_key = os.getenv(config['serper_api_key_env'])
groq_api_key = os.getenv(config['groq_api_key_env'])

def validate_email(email, keyword="consultation"):
    return keyword.lower() in email.lower()


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
        response = requests.post(url, headers=headers, data=payload, timeout=config["serper_timeout"])
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        # Try to get the first organic result's snippet
        if data.get('organic') and len(data['organic']) > 0:
            return data['organic'][0].get('snippet', 'No description found.')
        else:
            return "No search results found."

    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling Serper API: {e}")
        return "Could not retrieve company information."
    

# Initialize your Groq client
client = Groq(api_key=groq_api_key)
def call_api_with_retry(client, prompt, max_retries=None):
                    if max_retries is None:
                        max_retries = config["max_retries"]
                    for attempt in range(max_retries):
                       try:
                         response = client.chat.completions.create(
                         model="llama-3.3-70b-versatile",
                         messages=[{"role": "user", "content": prompt}])
                         return response.choices[0].message.content
                       except Exception as e:
                           logging.error(f"Attempt {attempt+1} failed: {e}")
                           if attempt == max_retries - 1:
                            raise  # re-raise the error after last attempt
                           wait_time = 2 ** attempt  # 1 second, then 2, then 4
                           logging.info(f"Waiting {wait_time} seconds before retry...")
                           time.sleep(wait_time)
# Open your output file
with open(config["output_file"], "w") as outfile:
    # Open and read your leads CSV
    with open(config["leads_file"], "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        
        # Load the last processed lead
        last_processed = load_checkpoint()
        processing = False


        for row in tqdm(rows, desc="Processing leads"):
            # Resume logic
            if not processing:
                if last_processed and row['name'] == last_processed:
                    processing = True
                continue  # skip until we find the checkpoint

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
                if not validate_email(email):
                    logging.info(f"Email for {row['name']} missing keyword. Retrying with stronger prompt.")
                    prompt += " Make sure to include the word 'consultation'."
                    email = call_api_with_retry(client, prompt, max_retries=2)
                # Write the email to the file
                outfile.write(f"--- Email for {row['name']} ---\n{email}\n\n")
                logging.info(f"Generated email for {row['name']}...")
                # Save checkpoint after successful processing
                save_checkpoint(row['name'])
            except Exception as e:
                logging.error(f"Failed to generate email for {row['name']}: {e}")
                outfile.write(f"--- Email for {row['name']} ---\nERROR: {e}\n\n")

               