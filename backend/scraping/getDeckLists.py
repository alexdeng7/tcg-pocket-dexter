import time
import csv
import os
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://play.limitlesstcg.com"
DECKS_URL = f"{BASE_URL}/decks?game=pocket"
CSV_OUTPUT = "data/rawDecklist.csv"

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

os.makedirs("data", exist_ok=True)
decklistData = []

driver.get(DECKS_URL)
time.sleep(2)

deckInfoList = []
while True:
    deckRows = driver.find_elements(By.CSS_SELECTOR, "tr[data-winrate]")
    for row in deckRows:
        try:
            linkEl = row.find_element(By.CSS_SELECTOR, "td:nth-child(3) a")
            href = linkEl.get_attribute("href")
            popularity = float(row.get_attribute("data-share"))
            winrate = float(row.get_attribute("data-winrate"))

            if href:
                deckInfoList.append({
                    "url": urljoin(BASE_URL, href),
                    "popularity": popularity,
                    "winrate": winrate
                })
        except Exception as e:
            print(f"Skipped a row: {e}")

    try:
        loadMore = driver.find_element(By.CSS_SELECTOR, "button.load-more")
        if loadMore.is_displayed():
            driver.execute_script("arguments[0].click();", loadMore)
            time.sleep(1.5)
        else:
            break
    except:
        break

print(f"Found {len(deckInfoList)} decks.")


def extractDeckLists():
    decklistDivs = driver.find_elements(By.CSS_SELECTOR, ".decklist .cards")
    decklist = []
    for section in decklistDivs:
        sectionName = section.find_element(
            By.CSS_SELECTOR, ".heading").text.strip()
        cards = section.find_elements(By.TAG_NAME, "p")
        for card in cards:
            decklist.append(f"{sectionName}: {card.text.strip()}")
    return decklist


print("\nScraping decks...")
for idx, deck in enumerate(deckInfoList):
    fullURL = deck["url"]
    try:
        driver.get(fullURL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "tr[data-player] td a[href*='decklist']")
            )
        )

        firstDeckEntry = driver.find_element(
            By.CSS_SELECTOR, "tr[data-player] td a[href*='decklist']")
        decklistURL = urljoin(BASE_URL, firstDeckEntry.get_attribute("href"))

        driver.get(decklistURL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".decklist"))
        )

        decklist = extractDeckLists()
        decklistData.append({
            "deck_url": fullURL,
            "decklist": " | ".join(decklist),
            "popularity": deck["popularity"],
            "winrate": deck["winrate"]
        })

        print(f"[{idx+1}/{len(deckInfoList)}] Scraped: {decklistURL}")

    except Exception as e:
        print(f"Error scraping {fullURL}: {e}")

with open(CSV_OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f, fieldnames=["deck_url", "decklist", "popularity", "winrate"])
    writer.writeheader()
    writer.writerows(decklistData)

print(f"\nSaved {len(decklistData)} decks to {CSV_OUTPUT}")

driver.quit()
