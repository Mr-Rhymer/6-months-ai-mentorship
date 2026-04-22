from flask import Flask, request
import json
import logging
import subprocess
import csv
import os
import sys
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
enrichment_script = os.path.join(script_dir, "enrich_leads_try.py")
leads_file = 'leads.csv'
app = Flask(__name__)

logging.basicConfig(filename='webhook.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/health', methods=['GET'])
def health():
    return {"status": "ok"}, 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        logging.info(f"Received: {data}")

        with open('received_data.json', 'a') as f:
            f.write(json.dumps(data) + '\n')

        # Append to CSV with timestamp
        file_exists = os.path.isfile(leads_file)
        with open(leads_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'company', 'industry', 'timestamp'])
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                'name': data.get('name', ''),
                'company': data.get('company', ''),
                'industry': data.get('industry', ''),
                'timestamp': datetime.now().isoformat()
            })
        logging.info(f"Appended lead to {leads_file}")

        # Run enrichment script
        with open("subprocess.log", "a") as log_file:
            result = subprocess.run(
                [sys.executable, enrichment_script],
                cwd=script_dir,
                capture_output=True,
                text=True
            )
            log_file.write(f"--- {datetime.now()} ---\n")
            log_file.write(f"STDOUT:\n{result.stdout}\n")
            log_file.write(f"STDERR:\n{result.stderr}\n")
            log_file.write(f"EXIT CODE: {result.returncode}\n\n")
            if result.returncode != 0:
                logging.error("Enrichment failed")
            else:
                logging.info("Enrichment succeeded")

        return "OK", 200
    except Exception as e:
        logging.error(f"Error: {e}")
        return "Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)