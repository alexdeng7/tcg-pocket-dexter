import fs from "fs";
import path from "path";
import express from "express";
import multer from "multer";
import cors from "cors";
import { exec } from "child_process";
import { fileURLToPath } from "url";
import Papa from "papaparse";

const app = express();
const port = 3001;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(cors());

const screenshotsPath = path.join(__dirname, "screenshots");
const croppedCardsPath = path.join(__dirname, "croppedCards");
const dataPath = path.join(__dirname, "data");
const topDeckCardsPath = path.join(__dirname, "topDeckCards");
const matchResultsPath = path.join(dataPath, "matchResults.csv");

const storage = multer.diskStorage({
  destination: screenshotsPath,
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}_${file.originalname}`);
  },
});
const upload = multer({ storage });

app.post("/upload", upload.single("screenshot"), (req, res) => {
  const matchScript = path.join(__dirname, "matching", "matchCards.py");

  exec(`python3 "${matchScript}"`, (error, stdout, stderr) => {
    if (error) {
      console.error("Python script error:", error);
      return res.status(500).json({ message: "Error running match script" });
    }

    console.log("Screenshot saved to", req.file.path);
    console.log("Matching Script Output:\n", stdout);

    res.json({ message: "Upload and matching complete!", file: req.file });
  });
});

app.get("/matched-card", (req, res) => {
  try {
    const csv = fs.readFileSync(matchResultsPath, "utf-8");
    const lines = csv.trim().split("\n");
    const headers = lines[0].split(",");
    const last = lines[lines.length - 1].split(",");

    const result = {
      cropped_card: last[headers.indexOf("cropped_card")],
      matched_card: last[headers.indexOf("matched_card")],
      hash_difference: last[headers.indexOf("hash_difference")],
    };

    res.json(result);
  } catch (err) {
    console.error("Failed to read matchResults.csv:", err);
    res.status(500).json({ error: "Failed to load match results" });
  }
});

app.get("/match-decks", (req, res) => {
  const scriptPath = path.join(__dirname, "matching", "matchDecks.py");

  exec(`python3 "${scriptPath}"`, (error, stdout, stderr) => {
    if (error) {
      console.error("Error running matchDecks.py:", error);
      return res.status(500).json({ error: "Deck matching failed." });
    }
    console.log("Deck matching complete:\n", stdout);
    res.json({ message: "Decks matched successfully." });
  });
});

app.get("/run-card-viewer", (req, res) => {
  const createDeckPath = path.join(__dirname, "matching", "createDeck.py");
  const matchSetsPath = path.join(__dirname, "matching", "matchSets.py");

  exec(
    `python3 "${createDeckPath}" && python3 "${matchSetsPath}"`,
    (error, stdout, stderr) => {
      if (error) {
        console.error("Error running card viewer scripts:", error);
        return res
          .status(500)
          .json({ error: "Card viewer generation failed." });
      }

      console.log("Card viewer scripts ran:\n", stdout);
      res.json({ message: "Deck images and sets prepared!" });
    }
  );
});

app.use("/croppedCards", express.static(croppedCardsPath));
app.use("/data", express.static(dataPath));
app.use("/topDeckCards", express.static(topDeckCardsPath));

app.listen(port, () => {
  console.log(`Backend server running on http://localhost:${port}`);
});

app.get("/get-deck-cards", (req, res) => {
  fs.readdir(topDeckCardsPath, (err, files) => {
    if (err) {
      console.error("Failed to read topDeckCards:", err);
      return res.status(500).json({ error: "Failed to read deck cards" });
    }

    const webpFiles = files.filter((f) => f.endsWith(".webp"));
    res.json(webpFiles);
  });
});

app.get("/get-pack-info", (req, res) => {
  const packCSV = path.join(dataPath, "openThesePacks.csv");

  fs.readFile(packCSV, "utf8", (err, data) => {
    if (err) {
      console.error("Failed to read openThesePacks.csv:", err);
      return res.status(500).json({ error: "Could not load pack info" });
    }

    const lines = data.trim().split("\n").slice(1);
    const parsed = lines
      .map((line) => line.split(","))
      .filter((row) => row.length === 3)
      .map(([Count, Card, Pack]) => ({ Count, Card, Pack }));

    res.json(parsed);
  });
});

app.post("/select-deck", express.json(), (req, res) => {
  const { index } = req.body;
  const decks = fs.readFileSync("data/decksMatched.csv", "utf8");
  const parsed = Papa.parse(decks, { header: true }).data;
  const selected = parsed[index];

  fs.writeFileSync("data/selectedDeck.json", JSON.stringify(selected));
  res.status(200).send("Deck selected");
});
