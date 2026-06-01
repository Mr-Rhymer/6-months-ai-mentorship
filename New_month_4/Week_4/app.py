import time
from groq import Groq
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import os
from functools import wraps

load_dotenv()
API_KEY = os.getenv("My_API_KEY", "your-local-default-key")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Received:", data)
    return jsonify({"status": "received", "data": data}), 200

@app.route('/secure_webhook', methods=['POST'])
@require_api_key
def secure_webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload"}), 400
    print("Authenticated data received:", data)
    return jsonify({"status": "authenticated", "data": data}), 200


client = Groq(api_key=GROQ_API_KEY)
def call_groq_with_retry(prompt, max_retries=3):
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

def truncate_text(text, max_chars=12000):
    if len(text) > max_chars:
        print(f"Text too long ({len(text)} chars). Truncating to {max_chars} chars.")
        return text[:max_chars]
    return text


@app.route('/ai_webhook', methods= ['POST'])
@require_api_key
def ai_webhook():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload"}), 400
    text = data.get("text")
    if not text: 
        return jsonify({"error": "Missing 'text' field in JSON payload"}), 400
    text = truncate_text(text)
    print("AI Webhook received:", data)
    prompt = f"Summarize the following text in 2-3 sentences:\n\n{text}"
    ai_summary = call_groq_with_retry(prompt)
    # Here you would add your AI processing logic
    ai_response = {"message": "AI processed your data", "input": data, "summary": ai_summary}
    return jsonify(ai_response), 200



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)