import os
import sys
import time
import csv
from time import sleep

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import get_html

BASE_URL = "https://www.rossmann.pl"

CATEGORIES = [
    "https://www.rossmann.pl/kategoria/wlosy/mycie-wlosow,13175?Page={}",
    "https://www.rossmann.pl/kategoria/wlosy/pielegnacja-wlosow,13181?Page={}"
]

OUTPUT_FILE = "data/product_links.csv"

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

def get_product_links(soup):
    product_links = []
    if soup is None:
        return product_links
    
    product_divs = soup.find_all("div", {"data-testid": "product-container"})
    for div in product_divs:
        a_tag = div.find("a", href=True)
        if a_tag:
            href = a_tag['href']
            if href.startswith("/Produkt/"):
                product_links.append(BASE_URL + href)
    return product_links
    
def scrape_all_categories():
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_link"])
            
    all_product_links = set()
    
    for index, category_template in enumerate(CATEGORIES, start=1):
        first_page_url = category_template.format(1)
        soup = get_html(first_page_url)
        last_page = get_last_page(soup)
        print(f" Found {last_page} pages in category {index}")
    
    for page_num in range(1, last_page + 1):
        page_url = category_template.format(page_num)
        print(f"Scraping page {page_num} of category {index}")
        
        soup = get_html(page_url)
        product_links = get_product_links(soup)
        print(f" Found {len(product_links)} products on page {page_num}")
        
        with open(OUTPUT_FILE, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for link in product_links:
                if link not in all_product_links:
                    writer.writerow([link])
                    all_product_links.add(link)
                    
        sleep(1)
    
if __name__ == "__main__":
    start_time = time.time()
    scrape_all_categories()
    end_time = time.time()
    print(f"Scraping completed in {end_time - start_time:.2f} seconds")
        
