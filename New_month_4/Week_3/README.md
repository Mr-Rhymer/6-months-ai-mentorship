# Project title: AI Lead Personalization (Serper + Groq)

# Description:
- Fetches live company info from Google Search via Serper API, then uses Groq to generate personalized outreach emails.

# Setup:
- Install groq, python-dotenv, requests;
- Add API keys to .env .

# How to run:
- python batch_lead_emailer.py (requires leads.csv with column company)

# Output files: 
- generated_emails.txt
- lead_emailer.log
- leads_emails.db