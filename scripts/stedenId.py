import os
import json
import time
import re
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

FB_C_USER = os.getenv("FB_C_USER")
FB_XS = os.getenv("FB_XS")

def get_region_id(place_name, page):
    # Ga naar Marketplace en zoek naar plaats
    print(f"🌍 Zoeken naar regio-ID voor: {place_name}")
    search_url = f"https://www.facebook.com/marketplace/search?query={place_name}"
    page.goto(search_url)
    page.wait_for_timeout(5000)

    # Haal de echte redirect-URL met regio-ID
    current_url = page.url
    match = re.search(r"/marketplace/(\d+)/", current_url)
    if match:
        return match.group(1)
    else:
        print(f"⚠️ Geen regio-ID gevonden voor: {place_name}")
        return None

def main():
    with open("./data/steden.txt", "r", encoding="utf-8") as f:
     places = [lijn.strip() for lijn in f if lijn.strip()]

    result = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ))

        context.add_cookies([
            {"name": "c_user", "value": FB_C_USER, "domain": ".facebook.com", "path": "/"},
            {"name": "xs", "value": FB_XS, "domain": ".facebook.com", "path": "/"}
        ])

        page = context.new_page()

        for place in places:
            region_id = get_region_id(place, page)
            if region_id:
                result[place] = region_id
            time.sleep(2)  # even vertragen tussen verzoeken

        browser.close()

    # Opslaan naar JSON
    with open("./data/regions.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        print("✅ Opgeslagen in regions.json")

if __name__ == "__main__":
    main()
