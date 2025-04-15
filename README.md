# Pokémon TCG Pocket: Dexter

Dexter is an AI-powered web application designed to enhance the experience of Pokémon TCG Pocket players. The app allows users to upload gameplay screenshots, automatically detect and identify cards, and receive competitive deck recommendations based on their current collection.

## Features

- Upload screenshots from the TCG Pocket game
- Automatically detect and crop cards using a custom-trained object detection model
- Match cropped cards to a local dataset of card art using perceptual hashing
- Recommend top competitive decks based on the matched cards
- Suggest which booster packs to open to complete missing cards in a selected deck
- Responsive, modern React frontend with smooth animations and clean styling

## How It Works

1. **Card Detection**  
   Uploaded screenshots are passed through a custom Roboflow object detection model to identify and crop each visible card.

2. **Card Matching**  
   Cropped cards are compared against a local dataset using perceptual hashing (`imagehash`) to determine the closest match.

3. **Deck Recommendation**  
   The system evaluates the matched cards against a curated database of competitive decks and suggests the best fits.

4. **Pack Suggestions**  
   For any cards missing from the selected deck, the app identifies which booster packs contain those cards.

## Tech Stack

- **Frontend**: React, Tailwind CSS, React Router
- **Backend**: Express (Node.js), Python (Pillow, imagehash)
- **AI Model**: Roboflow (custom-trained object detection)
- **Utilities**: Multer (image upload), Papaparse (CSV parsing), Pandas
