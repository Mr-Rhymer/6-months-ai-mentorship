from flask import Flask, request
import json
import logging
import subprocess  # to run another script
import csv
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
enrichment_script = os.path.join(script_dir, "enrich_leads_try.py")
leads_file = 'leads.csv'
file_exists = os.path.isfile(leads_file)
app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='webhook.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/webhook', methods=['POST'])
@app.route('/health', methods=['GET'])
def health():
    return {"status": "ok"}, 200
def webhook():
    """Receive POST data and process it."""
    try:
        # Get JSON data from the request
        data = request.get_json()
        logging.info(f"Received: {data}")
        
        # Save to a file (for later inspection)
        with open('received_data.json', 'a') as f:
            f.write(json.dumps(data) + '\n')
        
        # Optional: if the data contains a lead, run your enrichment script
        # For now, just return OK
            # Trigger lead enrichment (run as a subprocess)
        
        
        try:
               # Check existence inside the function each time
           file_exists = os.path.isfile(leads_file)
           with open(leads_file, 'a', newline='') as f:
             writer = csv.DictWriter(f, fieldnames=['name', 'company', 'industry'])
             if not file_exists:
                writer.writeheader()
             writer.writerow({
            'name': data.get('name', ''),
            'company': data.get('company', ''),
            'industry': data.get('industry', '')
                  })
           logging.info(f"Appended lead to {leads_file}")
        except Exception as e:
             logging.error(f"Error writing to CSV: {e}")
    
        try:
            subprocess.run([sys.executable, enrichment_script], check=True, cwd=script_dir, capture_output=True, text=True)
            logging.info("Lead enrichment completed successfully")
        except subprocess.CalledProcessError as e:
           logging.error(f"Enrichment failed (exit {e.returncode}): {e.stderr}")

        return "OK", 200
    except Exception as e:
           logging.error(f"Error: {e}")
           return "Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)