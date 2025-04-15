import os
import re

baseDir = os.path.dirname(os.path.abspath(__file__))
CARD_ART_DIR = os.path.join(baseDir, "..", "data", "cardArt")

for filename in os.listdir(CARD_ART_DIR):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        continue

    name, ext = os.path.splitext(filename)

    match = re.match(r"([A-Za-z0-9]+-\d+)[_\- ]+(.*)", name)
    if match:
        setNumber = match.group(1)
        cardName = match.group(2).replace("_", " ").strip()
        newName = f"{cardName} ({setNumber}){ext}"
        oldPath = os.path.join(CARD_ART_DIR, filename)
        newPath = os.path.join(CARD_ART_DIR, newName)
        os.rename(oldPath, newPath)
    else:
        print(f"Skipped: {filename} format not recognized")
