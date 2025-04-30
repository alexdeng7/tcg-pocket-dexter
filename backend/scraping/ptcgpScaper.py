from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import time

BASE_URL = "https://ptcgpocket.gg/cards"


def ptcgpScraper():
    os.makedirs("data", exist_ok=True)

    print("Loading website...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.get(BASE_URL)

    print("Loading the cards page...")

    SCROLL_PAUSE_TIME = 1.5
    MAX_SCROLL_ATTEMPTS = 80

    lastHeight = driver.execute_script("return document.body.scrollHeight")

    for i in range(MAX_SCROLL_ATTEMPTS):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        newHeight = driver.execute_script("return document.body.scrollHeight")

        if newHeight == lastHeight:
            print("Done loading all cards.")
            break
        lastHeight = newHeight

    print("Parsing the cards...")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    containers = soup.select('div.frontside')
    print(f"Found {len(containers)} card containers")

    cards = []
    for container in containers:
        style = container.get("style", "")
        match = re.search(r"url\((.*?)\)", style)
        imageURL = match.group(1) if match else None

        divName = container.find_parent(
            "a").find_next("div", class_="sc-fGdIVZ")
        cardName = divName.text.strip() if divName else "Unknown"

        if cardName and imageURL:
            cards.append({"name": cardName, "image_url": imageURL})
            print(f"{cardName}")

    df = pd.DataFrame(cards)
    df.to_csv("data/rawCards.csv", index=False)
    print(f"\nScraped {len(cards)} cards")


if __name__ == "__main__":
    print("Running scraper...")
    ptcgpScraper()
