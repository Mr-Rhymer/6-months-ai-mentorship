# AI Email Response Generator (Groq)

This project generates AI‑powered replies to emails using Groq's free LLM API.  
It supports multiple tones, stores responses in SQLite, processes batches from CSV, and exports to CSV.

## Features
- **Interactive mode** – paste an email, choose tone, get a reply.
- **Batch mode** – process multiple emails from a CSV file.
- **Tones** – formal, casual, informative, emphatic, urgent.
- **Confidence score** – each reply includes a confidence score (1‑10).
- **Database storage** – all interactions saved to `responses.db`.
- **CSV export** – export all replies to a timestamped CSV file.

## Setup
1. Install dependencies:
   ```bash
   pip install groq python-dotenv