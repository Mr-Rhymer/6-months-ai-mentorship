import requests
import json
import csv
import os
import time
import logging
from tqdm import tqdm
from groq import Groq
from dotenv import load_dotenv

# ========== 1. Load configuration ==========
with open("config.json", "r") as f:
    config = json.load(f)

# ========== 2. Setup logging ==========
logging.basicConfig(
    filename=config["log_file"],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ========== 3. Load API keys ==========
load_dotenv()
serper_api_key = os.getenv(config["serper_api_key_env"])
groq_api_key = os.getenv(config["groq_api_key_env"])

# ========== 4. Initialize Groq client ==========
client = Groq(api_key=groq_api_key)

# ========== 5. Checkpoint functions ==========
def load_checkpoint():
    try:
        with open(config["checkpoint_file"], "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_checkpoint(lead_name):
    with open(config["checkpoint_file"], "w") as f:
        f.write(lead_name)

# ========== 6. Serper API call ==========
def search_company_info(company_name):
    url = "https://google.serper.dev/search"
    payload = {"q": company_name}
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=config["serper_timeout"])
        response.raise_for_status()
        data = response.json()
        if data.get('organic') and len(data['organic']) > 0:
            return data['organic'][0].get('snippet', 'No description found.')
        else:
            return "No search results found."
    except Exception as e:
        logging.error(f"Serper API error for {company_name}: {e}")
        return "Could not retrieve company information."

# ========== 7. Groq API call with retry ==========
def call_groq_with_retry(prompt, max_retries=None):
    if max_retries is None:
        max_retries = config["max_retries"]
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

# ========== 8. Email validation ==========
def validate_email(email, keyword="consultation"):
    return keyword.lower() in email.lower()

# ========== 9. Main processing ==========
def main():
    # Load leads
    with open(config["leads_file"], "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Load checkpoint
    last_processed = load_checkpoint()
    processing = False

    # Open output file
    with open(config["output_file"], "w") as outfile:
        for row in tqdm(rows, desc="Processing leads"):
            # Resume logic
            if not processing:
                if last_processed and row['name'] == last_processed:
                    processing = True
                continue  # skip until we find the checkpoint

            # Get company info from Serper
            company_info = search_company_info(row['company'])

            # Build prompt
            prompt = f"""Write a short, professional email to {row['name']} at {row['company']} ({row['industry']}).
Here is some recent information I found about the company: {company_info}
The email should offer a free 15-minute consultation about AI automation.
Keep it under 100 words."""

            try:
                # Generate email
                email = call_groq_with_retry(prompt)
                
                # Validate keyword
                if not validate_email(email):
                    logging.info(f"Email for {row['name']} missing keyword. Retrying with stronger prompt.")
                    prompt += " Make sure to include the word 'consultation'."
                    email = call_groq_with_retry(prompt, max_retries=2)
                
                # Write to file
                outfile.write(f"--- Email for {row['name']} ---\n{email}\n\n")
                print(f"Generated email for {row['name']}")
                logging.info(f"Success for {row['name']}")
                
                # Save checkpoint
                save_checkpoint(row['name'])
                
            except Exception as e:
                error_msg = f"Failed for {row['name']}: {e}"
                print(error_msg)
                logging.error(error_msg)
                outfile.write(f"--- Email for {row['name']} ---\nERROR: {e}\n\n")

if __name__ == "__main__":
    main()