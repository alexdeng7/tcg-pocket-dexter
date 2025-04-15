import json
import os
import pandas as pd
import shutil
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
CARD_ART_DIR = os.path.join(DATA_DIR, "cardArt")
MATCHED_DECKS_PATH = os.path.join(DATA_DIR, "decksMatched.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "topDeckCards")

df = pd.read_csv(MATCHED_DECKS_PATH)
if df.empty:
    raise Exception("No matching decks found.")


SELECTED_PATH = os.path.join(DATA_DIR, "selectedDeck.json")
with open(SELECTED_PATH, "r") as f:
    topDeck = json.load(f)
pokemonCards = str(topDeck.get("pokemon", ""))
trainerCards = str(topDeck.get("trainers", ""))


def parseCards(cardList):
    cardEntries = []
    for entry in cardList.split(","):
        entry = entry.strip()
        match = re.match(r"(\d+)\s+(.*?)\s+\(([^)]+)\)", entry)
        if match:
            count = int(match.group(1))
            name = match.group(2)
            code = match.group(3)
            cardEntries.append((name, code, count))
        else:
            matchAlt = re.match(r"(\d+)\s+(.*)", entry)
            if matchAlt:
                count = int(matchAlt.group(1))
                name = matchAlt.group(2).strip()

                guessCode = None
                for file in os.listdir(CARD_ART_DIR):
                    filename = os.path.splitext(file)[0]
                    parts = filename.rsplit(" (", 1)
                    if len(parts) == 2:
                        namePart = parts[0].strip().lower()
                        if namePart == name.lower():
                            guessMatch = re.search(r"\((.*?)\)", file)
                            if guessMatch:
                                guessCode = guessMatch.group(1)
                                break

                cardEntries.append((name, guessCode, count))
            else:
                print(f"Skipped card: {entry}")
    return cardEntries


parsedCards = parseCards(pokemonCards) + parseCards(trainerCards)


def findCardImage(name, code=None):
    cleanName = name.strip()

    if code:
        match = re.match(r"([A-Za-z0-9]+)-(\d+)", code)
        if match:
            setPart = match.group(1)
            numPart = match.group(2).zfill(3)
            paddedCode = f"{setPart}-{numPart}".lower()
        else:
            paddedCode = code.lower()
        targetName = f"{cleanName} ({paddedCode})".lower()

        for file in os.listdir(CARD_ART_DIR):
            if os.path.splitext(file)[0].lower() == targetName:
                return file
    else:
        for file in os.listdir(CARD_ART_DIR):
            if cleanName.lower() in file.lower():
                return file

    return None


if os.path.exists(OUTPUT_DIR):
    for f in os.listdir(OUTPUT_DIR):
        fp = os.path.join(OUTPUT_DIR, f)
        if os.path.isfile(fp):
            os.remove(fp)

os.makedirs(OUTPUT_DIR, exist_ok=True)

copyCount = 0
for name, code, count in parsedCards:
    matchedCard = findCardImage(name, code)
    if not matchedCard:
        print(f"Image not found for: {name} ({code})")
        continue

    srcPath = os.path.join(CARD_ART_DIR, matchedCard)
    for i in range(1, count + 1):
        destFileName = f"{name} ({code}) {i}.webp" if code else f"{name} {i}.webp"
        destPath = os.path.join(OUTPUT_DIR, destFileName)
        shutil.copyfile(srcPath, destPath)
        copyCount += 1

print(f"\n{copyCount} cards are ready in this folder: {OUTPUT_DIR}")
