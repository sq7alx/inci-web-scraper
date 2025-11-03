import os
import sys
import json
import csv
import logging
from time import sleep
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.utils.helpers import get_html

LINKS_TO_SCRAPE_CSV = "data/product_links.csv"
OUTPUT_JSON = "data/products_data.json"

def parse_product(soup, url):
    name_div = soup.find("div", class_="h2 styles-module_titleName--0Nthy")
    name = name_div.get_text(strip=True) if name_div else None

    brand_div = soup.find("div", class_="styles-module_titleBrand--yLVXt")
    brand = None
    product_title = None
    if brand_div:
        a_tag = brand_div.find("a")
        if a_tag:
            brand = a_tag.get_text(strip=True)
            
    product_title = ''.join([t for t in brand_div.strings if t.strip() and t != brand]).strip()
    

    ingredients = None
    for section in soup.find_all("div", class_="styles-module_productDescriptionItem--GvY1O"):
        button = section.find("button", class_="styles-module_mobileTitleButton--o7AkB")
        if button and button.find("span") and "Składniki" in button.get_text():
            content_div = section.find("div", class_="styles-module_productDescriptionContent--76j9I")
            if content_div:
                p_tag = content_div.find("p")
                if p_tag:
                    ingredients_text = p_tag.get_text(strip=True)
                else:
                    ingredients_text = content_div.get_text(strip=True)

                # usuń prefix jeśli istnieje
                ingredients = re.sub(r'^(Ingredients:|Składniki:)\s*', '', ingredients_text, flags=re.IGNORECASE).strip()
            break

    # --- fallback, gdy nie znaleziono sekcji Składniki ---
    if not ingredients:
        for p in soup.find_all("p"):
            text = p.get_text(separator=" ", strip=True)
            if "Ingredients" in text or "Składniki" in text:
                span = p.find("span")
                if span:
                    ingredients_text = span.get_text(strip=True)
                else:
                    ingredients_text = text
                ingredients = re.sub(r'^(Ingredients:|Składniki:)\s*', '', ingredients_text, flags=re.IGNORECASE).strip()
                break

    ean = None
    for b in soup.find_all("b"):
        if "Kod EAN" in b.text:
            b_tag = soup.find("b", string=lambda t: "Kod EAN" in t)
            if b_tag:
                br_tag = b_tag.find_next("br")
                if br_tag:
                    ean = br_tag.get_text(strip=True)
            break

    return {
        "name": name,
        "product_title": product_title,
        "brand": brand,
        "ingredients": ingredients,
        "ean": ean,
        "url": url
    }

def scrape_inci():
    
    results = []
    
    with open(LINKS_TO_SCRAPE_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        product_links = [row["product_link"].strip('"') for row in reader if row["product_link"]]
    logging.info(f"Total product links to scrape: {len(product_links)}")
    
    for index, url in enumerate(product_links, start=1):
        print(f"Scraping product: {index} of {len(product_links)}")
        soup =  get_html(url)
        if not soup:
            logging.warning(f"Failed to load {url}")
            continue
        
        data = parse_product(soup, url)
        results.append(data)
    
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        sleep(1)
        
    # final save
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    logging.info(f"Scraping completed. Total products scraped: {len(results)}. Data saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    scrape_inci()