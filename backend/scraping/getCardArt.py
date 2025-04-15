import os
import pandas as pd
import requests
from tqdm import tqdm


def getCardArt(csv_path="data/rawCards.csv", output_dir="data/cardArt", force_download=False):
    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(csv_path)

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Downloading card art"):
        name = row['name'].replace(" ", "_").replace("/", "_")
        imageURL = row['image_url']
        ext = os.path.splitext(imageURL)[1].split("?")[0] or ".webp"

        cardID = imageURL.split("/")[-1].split(".")[0]
        filename = f"{cardID}__{name}{ext}"
        savePath = os.path.join(output_dir, filename)

        if os.path.exists(savePath) and not force_download:
            continue

        try:
            response = requests.get(imageURL, stream=True)
            if response.status_code == 200:
                with open(savePath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
            else:
                print(f"Failed to download {filename}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")

    print("All images downloaded.")


if __name__ == "__main__":
    getCardArt(force_download=True)
