from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from groq import Groq
from datetime import datetime
import sqlite3
import os
import csv
import io
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

DB_NAME = "clients.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            company TEXT,
            industry TEXT,
            sentiment TEXT,
            summary TEXT,
            priority INTEGER DEFAULT 5,
            status TEXT DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_contacted DATETIME,
            response_count INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_client(name, company, industry):
    prompt = f"""
    Analyze this new client:
    Name: {name}
    Company: {company}
    Industry: {industry}

    Return ONLY a valid JSON object with these exact keys:
    - "sentiment": one of "positive", "neutral", "negative"
    - "summary": a short 1-2 sentence professional summary
    - "priority": an integer from 1 to 10 (10 = highest priority)
    """
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "developer", "content": "Provide concise, accurate, and helpful responses. Always return valid JSON when requested."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

def generate_welcome_email(name, company, industry):
    prompt = f"""
    Write a short, warm, professional welcome email to a new client.

    Client Name: {name}
    Company: {company}
    Industry: {industry}

    Rules:
    - Maximum 140 words
    - Sound human and friendly
    - Express excitement to work with them
    - End with a clear next step
    - Return ONLY the email body (no subject line)
    """
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "developer", "content": "Provide concise, accurate, and helpful responses. Always return valid JSON when requested."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat()})

@app.route("/client", methods=["POST"])
def create_client():
    data = request.get_json() or {}

    name = data.get("name")
    email = data.get("email")
    company = data.get("company", "")
    industry = data.get("industry", "")

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    try:
        ai_result = analyze_client(name, company, industry)
        sentiment = ai_result.get("sentiment", "neutral")
        summary = ai_result.get("summary", "")
        priority = int(ai_result.get("priority", 5))
    except Exception:
        sentiment = "neutral"
        summary = "AI analysis unavailable"
        priority = 5

    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO clients 
        (name, email, company, industry, sentiment, summary, priority, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
    """, (name, email, company, industry, sentiment, summary, priority))
    
    client_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "id": client_id,
        "name": name,
        "email": email,
        "company": company,
        "industry": industry,
        "sentiment": sentiment,
        "summary": summary,
        "priority": priority,
        "status": "pending"
    }), 201

@app.route("/email", methods=["POST"])
def generate_email():
    data = request.get_json() or {}
    name = data.get("name")
    company = data.get("company", "")
    industry = data.get("industry", "")

    if not name:
        return jsonify({"error": "name is required"}), 400

    email_body = generate_welcome_email(name, company, industry)

    return jsonify({
        "subject": f"Welcome aboard, {name}!",
        "email_body": email_body
    })

@app.route("/report", methods=["GET"])
def export_report():
    conn = get_db()
    rows = conn.execute("SELECT * FROM clients ORDER BY priority DESC").fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id", "name", "email", "company", "industry",
        "sentiment", "summary", "priority", "status",
        "created_at", "last_contacted", "response_count"
    ])

    for row in rows:
        writer.writerow([dict(row)[col] for col in [
            "id", "name", "email", "company", "industry",
            "sentiment", "summary", "priority", "status",
            "created_at", "last_contacted", "response_count"
        ]])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="clients_report.csv"
    )

@app.route("/dashboard", methods=["GET"])
def dashboard():
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) as count FROM clients").fetchone()["count"]
    by_status = conn.execute("SELECT status, COUNT(*) as count FROM clients GROUP BY status").fetchall()
    by_industry = conn.execute("SELECT industry, COUNT(*) as count FROM clients GROUP BY industry").fetchall()
    recent = conn.execute("""
        SELECT id, name, company, priority, status, created_at 
        FROM clients ORDER BY created_at DESC LIMIT 10
    """).fetchall()
    conn.close()

    return jsonify({
        "total_clients": total,
        "by_status": {r["status"]: r["count"] for r in by_status},
        "by_industry": {(r["industry"] or "Unknown"): r["count"] for r in by_industry},
        "recent_clients": [dict(r) for r in recent]
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)