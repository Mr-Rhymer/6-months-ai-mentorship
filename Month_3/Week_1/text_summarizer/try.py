import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("ERROR: API key not found. Check your .env file.")
else:
    print(f"API key found: {api_key[:10]}...")

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents="Say 'Hello, world!'"
        )
        print("SUCCESS:", response.text)
    except ImportError as e:
        print("Import error:", e)
        print("Try: pip install google-genai")
    except Exception as e:
        print("Other error:", e)