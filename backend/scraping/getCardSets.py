import requests
from bs4 import BeautifulSoup
import csv
import os

url = 'https://game8.co/games/Pokemon-TCG-Pocket/archives/482685'

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')
rows = soup.find_all('tr')

cards = []

for row in rows:
    cols = row.find_all('td', class_='center')
    if len(cols) < 5:
        continue

    setTag = cols[1].find('b', class_='a-bold')
    setNum = setTag.text.strip() if setTag else None

    nameLink = cols[2].find('a', class_='a-link')
    cardName = nameLink.text.strip() if nameLink else None

    packSection = cols[4]
    bold = packSection.find('b', class_='a-bold')
    charName = None

    if bold:
        mainPack = bold.text.strip()
        br = bold.find_next('br')
        if br and br.next_sibling:
            charName = br.next_sibling.strip()

        if mainPack and charName:
            packName = f"{mainPack} {charName}"
        else:
            packName = mainPack
    else:
        packName = None

    if setNum and cardName and packName:
        cards.append({
            "Card Name": cardName,
            "Set Number": setNum,
            "Pack": packName,
        })

output = "data/cardSets.csv"
os.makedirs("data", exist_ok=True)

with open(output, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Card Name", "Set Number", "Pack"])
    writer.writeheader()
    writer.writerows(cards)

print(f"{len(cards)} cards saved to {output}")
