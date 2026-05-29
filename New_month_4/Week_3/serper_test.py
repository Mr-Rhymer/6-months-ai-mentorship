import os
from dotenv import load_dotenv
import requests


load_dotenv()
serper_api_key = os.getenv("SERPER_API_KEY")
if not serper_api_key:
    print("Error: SERPER_API_KEY not found in .env")
    exit(1)


def search_company(company_name):
        url = "https://google.serper.dev/search"
        payload = {"q": company_name}
        headers = {
            'X-API-KEY': serper_api_key,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
    
            if data.get('organic') and len(data['organic']) > 0:
                item = data['organic'][0]
                return {
                    'title': item.get('title', 'No title found.'),
                    'link': item.get('link', item.get('url', 'No link found.')),
                    'description': item.get('snippet', 'No description found.')
                }
            else:
                return {
                    'title': None,
                    'link': None,
                    'description': "No search results found."
                }
        except Exception as e:
            print(f"Serper API error for {company_name}: {e}")
            return {
                'title': None,
                'link': None,
                'description': "Could not retrieve company information."
            }           

if __name__ == "__main__":
    company_name = input("Enter a company name to search: ")
    result = search_company(company_name)
    print(f"Title: {result['title']}")
    print(f"Link: {result['link']}")
    print(f"Description: {result['description']}")