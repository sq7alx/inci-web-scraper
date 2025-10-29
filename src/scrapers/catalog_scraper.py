import json
from time import sleep
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import get_html

CATEGORIES = [
    "https://www.rossmann.pl/kategoria/wlosy/mycie-wlosow,13175?Page={}",
    "https://www.rossmann.pl/kategoria/wlosy/pielegnacja-wlosow,13181?Page={}"
]

all_product_links = []


def get_last_page(soup):
    last_page_span = soup.find("span", {"data-testid": "pagination-last-page"})
    if last_page_span and last_page_span.get_text().isdigit():
        try:
            return int(last_page_span.get_text())
        except ValueError:
            pass
        
    pagination = soup.find("ul", class_="pagination")
    if pagination:
        page_numbers = [int(a.get_text()) for a in pagination.find_all("a") if a.get_text().isdigit()]
        if page_numbers:
            print("page_numbers:", page_numbers)
            return max(page_numbers)
    return 1

for category_template in CATEGORIES:
    url = category_template.format(1)
    html = get_html(url)
    last_page = get_last_page(html)
    print(last_page)
