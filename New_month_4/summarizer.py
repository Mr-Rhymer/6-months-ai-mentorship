from groq import Groq
import os
from dotenv import load_dotenv
import time

load_dotenv()
try:
    client = Groq(api_key=os.getenv("GROK_API_KEY_2"))
except Exception as e:
    print(f"Error initializing Groq client: {e}")

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None

def summarize_with_retry(text, max_retries=3):
    def truncate_text(text, max_chars=12000):
        if len(text) > max_chars:
            print(f"Text too long ({len(text)} chars). Truncating to {max_chars} chars.")
            return text[:max_chars]
        return text

    text = truncate_text(text)
    prompt = f"Summarize the following text in 2-3 sentences:\n\n{text}"
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # exponential backoff

def save_summary(summary, original_filename):
    base, ext = os.path.splitext(original_filename)
    out_filename = f"{base}_summary.txt"
    with open(out_filename, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"Summary saved to {out_filename}")

def main():
    filename = input("Enter text file name: ")
    text = read_file(filename)
    if text is None:
        return
    try:
        summary = summarize_with_retry(text)
        print("\n--- Summary ---\n")
        print(summary)
        save_summary(summary, filename)
    except Exception as e:
        print(f"Failed to summarize: {e}")

if __name__ == "__main__":
    main()
