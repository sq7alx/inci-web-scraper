import os
import sys
import time
import logging
import subprocess
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

def run_script(script_path):
    start = time.time()
    
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    
    if result.returncode != 0:
        logging.error(f"Error running {script_path}")
        logging.error(result.stderr)
    else:
        logging.info(f"Finished running {script_path} in {time.time() - start:.2f} seconds")
        logging.info(result.stdout)

def has_records(csv_path):
    if not os.path.exists(csv_path):
        return False
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
        return len(rows) > 1
    
def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    scrapers_dir = os.path.join(base_dir, "src", "scrapers")
    
    catalog_scraper = os.path.join(scrapers_dir, "catalog_links_scraper.py")
    product_scraper = os.path.join(scrapers_dir, "product_inci_scraper.py")
    
    links_csv = os.path.join(base_dir, "data", "product_links.csv")
                                   
    if has_records(links_csv):
        answer = input("Found records in product_links.csv. Do you want to download the links again? (y/n): ").strip().lower()
        if answer == "y":
            logging.info("Starting cosmetics links scraper...")
            run_script(catalog_scraper)
        else:
            logging.info("Skipping catalog re-scraping")
    else:
        logging.info("Starting cosmetics links scraper..")
        run_script(catalog_scraper)

    logging.info("Starting cosmetics ingredients scraper...")
    run_script(product_scraper)
    
    logging.info("All scraping completed")
        
if __name__ == "__main__":
    main()
    
    
