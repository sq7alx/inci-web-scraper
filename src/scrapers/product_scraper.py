import json
from time import sleep
import argparse

from src.utils.helpers import get_html

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
    for p in soup.find_all("p"):
        if "Ingredients:" in p.get_text():
            span = p.find("span")
            if span:
                ingredients = span.get_text(strip=True)
            else:
                full_text = p.get_text(separator=" ", strip=True)
                ingredients = full_text.split("Ingredients:")[1].strip()
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
    
def main():
    parser = argparse.ArgumentParser(description="Rossmann product scraper")
    parser.add_argument("--base-url", required=True, help="Base URL for Rossmann products")
    args = parser.parse_args()
    
    results = []
    soup = get_html(args.base_url)
    if soup:
        data = parse_product(soup, args.base_url)
        results.append(data)
    sleep(1)

    with open("output_test.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
            
if __name__ == "__main__":
    main()