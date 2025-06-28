from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import json
load_dotenv()

FB_C_USER = os.getenv("FB_C_USER")
FB_XS = os.getenv("FB_XS")

def scrape_marketplace(query, region_id, max_price):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ))

        # Voeg sessiecookies toe
        context.add_cookies([
            {"name": "c_user", "value": FB_C_USER, "domain": ".facebook.com", "path": "/"},
            {"name": "xs", "value": FB_XS, "domain": ".facebook.com", "path": "/"}
        ])

        page = context.new_page()
        url = f"https://www.facebook.com/marketplace/{region_id}/search?maxPrice={max_price}&query={query}&exact=false"
        print(f"🔍 Openen: {url}")
        page.goto(url)
        page.wait_for_selector("a[href^='/marketplace/item/']", timeout=15000)

        # Screenshot voor debug
        page.screenshot(path="debug.png", full_page=True)
        print("📸 Screenshot opgeslagen als debug.png")

        # Scrape item-kaarten
        cards = page.query_selector_all("a[href^='/marketplace/item/']")
        print(f"🔎 Gevonden zoekertjes: {len(cards)}")

        seen_links = set()

        for card in cards[:5]:
            try:
                href = card.get_attribute("href")
                if not href or href in seen_links:
                    continue
                seen_links.add(href)

                link = f"https://www.facebook.com{href}"
                tekst = card.inner_text()
                lijnen = tekst.split('\n')

                prijs = lijnen[0] if len(lijnen) > 0 else "?"
                titel = lijnen[1] if len(lijnen) > 1 else "?"
                locatie = lijnen[2] if len(lijnen) > 2 else "?"

                img_tag = card.query_selector("img")
                afbeelding = img_tag.get_attribute("src") if img_tag else "geen afbeelding"

                print("📦 ITEM")
                print(f"🔗 Link     : {link}")
                print(f"💶 Prijs    : {prijs}")
                print(f"📄 Titel    : {titel}")
                print(f"📌 Locatie  : {locatie}")
                print(f"🖼️ Afbeelding: {afbeelding}")
                print("-" * 50)

            except Exception as e:
                print("⚠️ Fout bij verwerken item:", e)

        browser.close()

# Testcode
# Testcode
if __name__ == "__main__":
    import json

    # Laad regio-ID's uit JSON
    with open("data/regions.json", "r", encoding="utf-8") as f:
        REGIO_IDS = json.load(f)

    print("📍 Beschikbare regio's:", ', '.join(REGIO_IDS.keys()))
    regio_naam = input("➡️  Welke regio wil je gebruiken? ").strip()

    regio_id = REGIO_IDS.get(regio_naam)
    if not regio_id:
        print(f"❌ Geen regio-ID gevonden voor: {regio_naam}")
    else:
        zoekterm = input("🔎 Wat wil je zoeken? ").strip()
        max_price = input("💰 Maximumprijs (bv. 200): ").strip()

        if not max_price.isdigit():
            print("❌ Ongeldige prijs ingevoerd.")
        else:
            scrape_marketplace(zoekterm, regio_id, max_price)

