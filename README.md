# 🛒 MarketplaceBot v1

A Python project that automatically scans Facebook Marketplace based on your preferences (location, keyword, and max price), then displays the top results in the terminal.

## ⚙️ Features

- Choose a city from a list (e.g., Gent, Brugge, Eeklo, ...).
- Provide a keyword (e.g., "bike", "rtx", "chair").
- Set a maximum price (e.g., €200).
- See the top 5 results, including:
  - Title
  - Price
  - Location
  - Link to the item
  - Image (URL)

## 🧱 Project Structure

```plaintext
MarketplaceBot/
├── data/
│   ├── regions.json          # Region IDs generated from city names
│   └── steden.txt            # List of city names (input)
├── discordbot/               # (Placeholder for future Discord bot)
├── scraper/
│   └── facebookScraper.py    # The main scraper
├── scripts/
│   └── stedenId.py           # Generates region IDs using steden.txt
├── .env                      # Facebook session cookies
├── .gitignore
├── debug.png                 # Debug screenshot from the scraper
├── main.py                   # Entry point (for future use or integration)
├── requirements.txt          # Required Python packages
└── README.md
```

## 🚀 Installation

1. **Clone this repository**

```bash
git clone https://github.com/yourusername/MarketplaceBot.git
cd MarketplaceBot
```

2. **Install the required packages**

Ensure you have Python 3.10+. Then run:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
playwright install
```

3. **Add your Facebook cookies**

Create a `.env` file with your session cookies:

```env
FB_C_USER=your_cookie_c_user
FB_XS=your_cookie_xs
```

> ⚠️ You can get these from browser devtools > Application > Cookies > facebook.com

4. **Generate region IDs**

Edit `data/steden.txt` with your preferred cities, then run:

```bash
python scripts/stedenId.py
```

This will create `regions.json` with valid region IDs.

---

## ✅ Usage

Run the scraper:

```bash
python scraper/facebookScraper.py
```

You’ll be prompted to:

- Select a region from `regions.json`
- Enter a keyword
- Set a maximum price

Up to 5 relevant items will be shown in the terminal.

---

## 🔮 Future ideas (v2, v3...)

- [ ] Support for multiple keywords
- [ ] Scraping across multiple regions
- [ ] Save results to JSON or CSV
- [ ] Send notifications to Discord
- [ ] Build a web interface

---

## 📜 License

MIT License — feel free to use and extend.

---

**Created by [your name or GitHub handle]**
