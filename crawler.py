import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Configure requests to use Tor SOCKS proxy
session = requests.Session()
session.proxies = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}

def fetch_metadata(url):
    try:
        response = session.get(url, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else None
        text_snippet = " ".join(soup.stripped_strings)[:200]  # first 200 characters

        return {
            "url": url,
            "status_code": response.status_code,
            "title": title,
            "content_length": len(response.content),
            "text_snippet": text_snippet,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "url": url,
            "status_code": None,
            "title": None,
            "content_length": None,
            "text_snippet": None,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }