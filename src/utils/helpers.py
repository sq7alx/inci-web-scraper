import requests
from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_html(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        with open("html.txt",  "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        return soup
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None