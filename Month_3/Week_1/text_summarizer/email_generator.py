from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Paste the email you received (press Enter twice to finish):")
lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)
received_email = "\n".join(lines)

tone = input("What tone? (professional/friendly/apologetic): ").strip().lower()

prompt = f"""You are an AI email assistant. Write a {tone} reply to the following email.

--- Received email ---
{received_email}
--- End of email ---

Your reply should be clear, polite, and address all key points. Write only the email body, no extra text."""
try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message.content
except Exception as e:
    print(f"Error generating email reply: {e}")
print("\n--- Generated Reply ---\n")
print(reply)

save = input("\nSave this reply to file? (y/n): ").lower()
if save == 'y':
    with open("email_reply.txt", "w") as f:
        f.write(reply)
    print("Saved to email_reply.txt")