import os
import time
import traceback
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)

# Environment variables
API_KEY = os.getenv("MY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def call_groq_with_retry(prompt, max_retries=3):
    """Call Groq API with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # free, fast, reliable
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

def truncate_text(text, max_chars=12000):
    """Truncate text to safe length for token limits."""
    if len(text) > max_chars:
        print(f"Truncating text from {len(text)} to {max_chars} chars")
        return text[:max_chars]
    return text

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/ai_webhook', methods=['POST'])
def ai_webhook():
    # 1. Authenticate
    provided_key = request.headers.get('X-API-Key')
    if provided_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # 2. Parse and validate JSON
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload"}), 400

    text = data.get("text")
    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    # 3. Truncate if too long
    text = truncate_text(text)

    # 4. Build prompt
    prompt = f"Summarize the following text in 2-3 sentences:{text}"

    # 5. Call Groq with retry
    try:
        summary = call_groq_with_retry(prompt)
        return jsonify({"summary": summary}), 200
    except Exception as e:
        # Log full error (visible in Render logs)
        print("=" * 60)
        print("ERROR in /ai_webhook:")
        traceback.print_exc()
        print("=" * 60)
        return jsonify({"error": str(e)}), 500
    

@app.route('/sentiment', methods=['POST'])
def sentiment():
    # 1. Authenticate
    provided_key = request.headers.get('X-API-Key')
    if provided_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # 2. Parse and validate JSON
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload"}), 400

    text = data.get("text")
    if not text:
        return jsonify({"error": "Missing 'text' field"}), 400

    # 3. Truncate if needed
    text = truncate_text(text)

    # 4. Build the sentiment prompt
    prompt = f"""Analyze the sentiment of the following customer feedback.
Return ONLY a valid JSON object with these three fields:
- "sentiment": one of "positive", "neutral", or "negative"
- "confidence": a number from 1 to 10
- "summary": a one-sentence summary of the feedback

Feedback: {text}

Output only valid JSON, no other text."""

    # 5. Call Groq and parse the response
    try:
        raw_response = call_groq_with_retry(prompt)
        import json
        result = json.loads(raw_response)
        return jsonify(result), 200
    except Exception as e:
        print("Error in /sentiment:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
