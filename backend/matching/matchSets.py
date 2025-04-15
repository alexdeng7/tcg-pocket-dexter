import pandas as pd
import re
import os
import unicodedata
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

deckCSV = os.path.join(DATA_DIR, "decksMatched.csv")
setCSV = os.path.join(DATA_DIR, "cardSets.csv")
output = os.path.join(DATA_DIR, "openThesePacks.csv")

deckDF = pd.read_csv(deckCSV)
setDF = pd.read_csv(setCSV)

if deckDF.empty:
    raise Exception("No matching decks found.")

SELECTED_PATH = os.path.join(DATA_DIR, "selectedDeck.json")
with open(SELECTED_PATH, "r") as f:
    topDeck = json.load(f)
pokeCards = str(topDeck.get("pokemon", ""))
otherCards = str(topDeck.get("trainers", ""))


def normalizeName(name):
    if not isinstance(name, str):
        return ""
    return unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("utf-8").lower().strip()


def parseCards(card_list):
    entries = []
    for entry in card_list.split(","):
        entry = entry.strip()
        match = re.match(r"(\d+)\s+(.*?)\s+\(([^)]+)\)", entry)
        if match:
            count = int(match.group(1))
            name = match.group(2)
            code = match.group(3).replace("–", "-")
            entries.append((name, code, count))
        else:
            matchAlt = re.match(r"(\d+)\s+(.*)", entry)
            if matchAlt:
                count = int(matchAlt.group(1))
                name = matchAlt.group(2).strip()
                code = None
                entries.append((name, code, count))
            else:
                print(f"Skipped card: {entry}")
    return entries


parsedCards = parseCards(pokeCards) + parseCards(otherCards)


def normalizeSet(setNum):
    match = re.match(r"([A-Za-z0-9]+)\s*(\d+)", setNum)
    if match:
        setCode = match.group(1)
        num = match.group(2).zfill(3)
        return f"{setCode}-{num}"
    return setNum


setDF["Normalized Set"] = setDF["Set Number"].apply(normalizeSet)

outputRows = []


def normalizeDeckCode(deckCode):
    if not deckCode:
        return None
    match = re.match(r"([A-Za-z0-9]+)-(\d+)", deckCode)
    if match:
        setPart = match.group(1)
        numPart = match.group(2).zfill(3)
        return f"{setPart} {numPart}"
    return deckCode


for name, code, count in parsedCards:
    normalizedCode = normalizeDeckCode(code) if code else None
    normalizedName = normalizeName(name)

    if normalizedCode:
        matchRow = setDF[
            (setDF["Card Name"].apply(normalizeName) == normalizedName) &
            (setDF["Set Number"].str.strip().str.upper()
             == normalizedCode.upper())
        ]
    else:
        matchRow = pd.DataFrame()

    if matchRow.empty:
        nameMatch = setDF[
            setDF["Card Name"].apply(normalizeName) == normalizedName
        ]
        if not nameMatch.empty:
            pack = nameMatch.iloc[0]["Pack"]
        else:
            pack = "Not Found"
    else:
        pack = matchRow.iloc[0]["Pack"]

    outputRows.append({
        "Count": count,
        "Card": f"{name} ({code})",
        "Pack": pack
    })

finalDF = pd.DataFrame(outputRows).sort_values(by="Pack")

os.makedirs("data", exist_ok=True)
finalDF.to_csv(output, index=False)

print(f"{len(outputRows)} cards saved to {output}")
