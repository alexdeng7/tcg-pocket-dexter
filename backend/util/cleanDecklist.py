import pandas as pd
import os

baseDir = os.path.dirname(os.path.abspath(__file__))
dataDir = os.path.join(baseDir, "..", "data")

inputCSV = os.path.join(dataDir, "rawDecklist.csv")
outputCSV = os.path.join(dataDir, "finalDecklists.csv")

df = pd.read_csv(inputCSV)
cleanedRows = []

for _, row in df.iterrows():
    url = row["deck_url"]
    decklist = row["decklist"].split(" | ")
    popularity = row.get("popularity", None)
    winrate = row.get("winrate", None)

    pokemon = []
    trainers = []

    for entry in decklist:
        if entry.startswith("Pokémon"):
            pokemon.append(entry.split(": ")[-1])
        elif entry.startswith("Trainer"):
            trainers.append(entry.split(": ")[-1])

    cleanedRows.append({
        "deck_url": url,
        "pokemon": ", ".join(pokemon),
        "trainers": ", ".join(trainers),
        "popularity": popularity,
        "winrate": winrate
    })

cleanedDF = pd.DataFrame(cleanedRows)
cleanedDF.to_csv("data/finalDecklists.csv", index=False)
