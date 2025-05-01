from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

options = Options()

options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get("https://play.limitlesstcg.com/decks?game=pocket")
time.sleep(2)

deckURLs = set()
MAX_SCROLLS = 5
scrolls = 0

while scrolls < MAX_SCROLLS:
    deckContents = driver.find_elements(
        By.CSS_SELECTOR, 'tr[data-winrate] td:nth-child(3) a')
    for el in deckContents:
        href = el.get_attribute("href")
        if href:
            deckURLs.add("https://play.limitlesstcg.com" + href)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    scrolls += 1

driver.quit()

print(f"Scraped {len(deckURLs)} decks")

with open("data/deckURLs.csv", "w") as f:
    for url in sorted(deckURLs):
        f.write(url + "\n")
