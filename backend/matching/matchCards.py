import os
import cv2
import imagehash
import pandas as pd
from PIL import Image
from tqdm import tqdm
from inference_sdk import InferenceHTTPClient
import glob

API_URL = "https://detect.roboflow.com"
API_KEY = "Y4M1BoiD0IeWJLfabNVH"
WORKSPACE = "ptcgp"
WORKFLOW = "card-detector-two"
STANDARD_WIDTH = 359
STANDARD_HEIGHT = 782

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCREENSHOT_DIR = os.path.join(ROOT_DIR, "screenshots")
CROP_OUTPUT_DIR = os.path.join(ROOT_DIR, "croppedCards")
CARD_ART_DIR = os.path.join(ROOT_DIR, "data", "cardArt")
CSV_OUTPUT = os.path.join(ROOT_DIR, "data", "matchResults.csv")
TEMP_IMAGE_PATH = os.path.join(ROOT_DIR, "temp.jpeg")

imageFiles = sorted(
    glob.glob(os.path.join(SCREENSHOT_DIR, "*")),
    key=os.path.getmtime,
    reverse=True
)
if not imageFiles:
    raise Exception("No screenshot found")
INPUT_IMAGE = imageFiles[0]
print(f"Selected last uploaded: {INPUT_IMAGE}")

os.makedirs(CROP_OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CSV_OUTPUT), exist_ok=True)

for f in os.listdir(CROP_OUTPUT_DIR):
    fp = os.path.join(CROP_OUTPUT_DIR, f)
    if os.path.isfile(fp):
        os.remove(fp)

original = cv2.imread(INPUT_IMAGE)
if original is None:
    raise Exception(f"Failed to read input image at {INPUT_IMAGE}")

resized = cv2.resize(original, (STANDARD_WIDTH, STANDARD_HEIGHT))

client = InferenceHTTPClient(api_url=API_URL, api_key=API_KEY)
cv2.imwrite(TEMP_IMAGE_PATH, resized)
result = client.run_workflow(
    workspace_name=WORKSPACE,
    workflow_id=WORKFLOW,
    images={"image": TEMP_IMAGE_PATH},
    use_cache=True
)
os.remove(TEMP_IMAGE_PATH)

predictions = result[0]['predictions']['predictions']
print(f"{len(predictions)} cards found\n")

croppedPaths = []
for idx, pred in enumerate(predictions):
    xCenter, yCenter = int(pred['x']), int(pred['y'])
    width, height = int(pred['width']), int(pred['height'])
    x1 = max(0, xCenter - width // 2)
    y1 = max(0, yCenter - height // 2)
    x2 = min(x1 + width, resized.shape[1])
    y2 = min(y1 + height, resized.shape[0])

    cropped = resized[y1:y2, x1:x2]
    savePath = os.path.join(CROP_OUTPUT_DIR, f"card_{idx + 1}.png")
    cv2.imwrite(savePath, cropped)
    croppedPaths.append(savePath)
    print(f"Card saved: {savePath}")


def computeHashes(imagePath):
    image = Image.open(imagePath).convert("RGB")
    return {
        "ahash": imagehash.average_hash(image),
        "phash": imagehash.phash(image),
        "dhash": imagehash.dhash(image),
        "whash": imagehash.whash(image)
    }


def hashDistance(hash1, hash2):
    return sum(h1 - h2 for h1, h2 in zip(hash1.values(), hash2.values()))


print("\nParsing Through cardArt...")
cardHashes = {}
for filename in tqdm(os.listdir(CARD_ART_DIR)):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        try:
            path = os.path.join(CARD_ART_DIR, filename)
            cardHashes[filename] = computeHashes(path)
        except Exception as e:
            print(f"Skipped {filename}: {e}")

print("\nMatching cards...")
matchData = []

for path in croppedPaths:
    try:
        cropHash = computeHashes(path)
    except Exception as e:
        print(f"Failed to hash {path}: {e}")
        continue

    bestMatch = None
    lowestScore = float("inf")
    for name, cardHash in cardHashes.items():
        score = hashDistance(cropHash, cardHash)
        if score < lowestScore:
            lowestScore = score
            bestMatch = name

    print(f"{os.path.basename(path)} → {bestMatch} (diff: {lowestScore})")
    matchData.append({
        "cropped_card": os.path.basename(path),
        "matched_card": bestMatch,
        "hash_difference": lowestScore
    })

df = pd.DataFrame(matchData)
df.to_csv(CSV_OUTPUT, index=False)
print(f"\nMatching complete. Results saved to: {CSV_OUTPUT}")
