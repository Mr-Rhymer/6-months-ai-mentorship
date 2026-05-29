from groq import Groq
from dotenv import load_dotenv
import json
import time
import os
import requests
from serper_test import search_company

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

client = Groq(api_key=groq_api_key)
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



if __name__ == "__main__":
   company_name = input("Enter the company name: ")
   info = search_company(company_name) 
   description = info['description'] 
   if description:
       
      prompt = f"""Write a short professional email to {company_name} with the description: {description} to offer a free AI consultation. 
   The email should be concise, engaging, and include a clear call to action for scheduling the consultation.
   It should be under 150 words and tailored to the company's industry and needs."""
   else:
      prompt = f"""Write a short professional email to {company_name} to offer a free AI consultation.
   The email should be concise, engaging, and include a clear call to action for scheduling the consultation.
   It should be under 150 words and tailored to the company's industry and needs."""
   reply = call_groq_with_retry(prompt, max_retries=3)
   print("\nGenerated Email:\n")
   print(reply)