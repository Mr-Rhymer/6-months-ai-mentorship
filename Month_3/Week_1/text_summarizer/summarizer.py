from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Paste your text below (press Enter twice to finish):")
lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)
text = "\n".join(lines)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # fast, free model
    messages=[{"role": "user", "content": f"Summarize this in 2-3 sentences:\n\n{text}"}]
)
print("\n--- Summary ---")
print(response.choices[0].message.content)