import pandas as pd
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

matchPath = os.path.join(DATA_DIR, "matchResults.csv")
deckPath = os.path.join(DATA_DIR, "finalDecklists.csv")
outputPath = os.path.join(DATA_DIR, "decksMatched.csv")

matchDF = pd.read_csv(matchPath)
deckDF = pd.read_csv(deckPath)


def getPrefix(cardString):
    match = re.match(r"(.*?)\s+\(([A-Za-z0-9]+)-\d+\)", cardString)
    if match:
        name = match.group(1).strip().lower()
        prefix = match.group(2).strip().upper()
        return (name, prefix)
    return None


matchSet = matchDF["matched_card"].dropna().apply(
    lambda x: re.sub(r"\.webp$", "", x.strip())
).map(getPrefix).dropna().tolist()


def normalizeDeckCard(card):
    fullMatch = re.match(r"\d+\s+(.*?)\s+\(([A-Za-z0-9]+)-\d+\)", card)
    if fullMatch:
        name = fullMatch.group(1).strip().lower()
        prefix = fullMatch.group(2).strip().upper()
        return (name, prefix)

    nameOnly = re.match(r"\d+\s+(.*)", card)
    if nameOnly:
        return (nameOnly.group(1).strip().lower(), None)

    return None


def deckMatched(row):
    allCards = []
    if pd.notna(row.get("pokemon")):
        allCards += row["pokemon"].split(", ")
    if pd.notna(row.get("trainers")):
        allCards += row["trainers"].split(", ")

    normalizedCards = [normalizeDeckCard(card.strip()) for card in allCards]

    for card in normalizedCards:
        if not card:
            continue
        name, prefix = card
        for matchName, matchPrefix in matchSet:
            if name == matchName and (prefix == matchPrefix or prefix is None):
                return True
    return False


matchedDecks = deckDF[deckDF.apply(deckMatched, axis=1)].copy()

matchedDecks["popularity"] = pd.to_numeric(
    matchedDecks.get("popularity", 0), errors="coerce")
matchedDecks["winrate"] = pd.to_numeric(
    matchedDecks.get("winrate", 0), errors="coerce")
matchedDecks = matchedDecks.sort_values(
    by=["popularity", "winrate"], ascending=[False, False])

matchedDecks.to_csv(outputPath, index=False)

print("\nDecks with your card/cards:")
print(matchedDecks[["pokemon", "trainers", "popularity", "winrate"]])
print(f"\nSaved to: {outputPath}")
