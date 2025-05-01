import { useState } from "react";
import { useNavigate } from "react-router-dom";
import pokeball from "./assets/pokeball-spin.gif";
import "./index.css";

function App() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [progress, setProgress] = useState("");
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setProgress("Currently uploading...");

    const formData = new FormData();
    formData.append("screenshot", file);

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      await new Promise((r) => setTimeout(r, 1000));
      setProgress("Analyzing your screenshot...");

      await new Promise((r) => setTimeout(r, 1500));
      setProgress("Searching card database...");

      await new Promise((r) => setTimeout(r, 1000));
      setProgress("Card found.");

      const data = await res.json();
      setMessage("Upload and matching complete.");
      navigate("/results");
    } catch {
      setMessage("Upload failed, please try again with a new screenshot.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="w-screen min-h-screen bg-gradient-to-br from-yellow-100 via-red-200 to-pink-300 flex flex-col justify-center items-center text-center text-gray-800 px-4 py-12 relative overflow-hidden">
      <img
        src={pokeball}
        alt="Pokéball"
        className="w-84 h-auto animate-float glow-pokeball z-10 drop-shadow-2xl"
      />

      <h1 className="text-5xl md:text-6xl font-extrabold text-red-600 drop-shadow-xl animate-pulse mb-6 font-pokemon">
        Pokémon TCG Pocket Dexter
      </h1>

      <div className="bg-white/50 backdrop-blur-lg p-8 md:p-10 rounded-3xl shadow-xl border border-white/20 max-w-xl w-full">
        <p className="text-lg md:text-xl text-gray-700 mb-6">
          Upload a screenshot with a card, and let us help you find the best
          decks to play with!
        </p>

        <input
          type="file"
          accept="image/*"
          id="screenshot-upload"
          className="hidden"
          onChange={(e) => {
            setFile(e.target.files[0]);
            setMessage("");
            setProgress("");
          }}
        />

        <label
          htmlFor="screenshot-upload"
          className="block w-full text-center bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-6 rounded-full cursor-pointer transition duration-300 mb-4"
        >
          {file ? "Change Screenshot" : "Choose Screenshot"}
        </label>

        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className={`w-full text-white font-semibold py-3 px-6 rounded-full transition duration-300 shadow-md text-lg ${
            file
              ? "bg-gradient-to-r from-pink-500 via-red-500 to-yellow-400 hover:from-yellow-400 hover:to-pink-500"
              : "bg-gray-300 cursor-not-allowed"
          }`}
        >
          {uploading ? "Processing..." : "Upload Screenshot"}
        </button>

        {progress && (
          <p className="mt-4 text-sm text-gray-800 animate-pulse">{progress}</p>
        )}
        {message && (
          <p className="mt-2 text-sm font-semibold text-gray-900">{message}</p>
        )}
      </div>

      <p className="mt-10 text-sm text-gray-600 italic z-10">
        Built by Alex Deng
      </p>
      <div className="absolute top-[-50px] left-[-50px] w-72 h-72 bg-pink-300 opacity-30 rounded-full blur-3xl animate-spin-slow z-0" />
      <div className="absolute bottom-[-50px] right-[-50px] w-72 h-72 bg-yellow-300 opacity-30 rounded-full blur-3xl animate-pulse z-0" />
    </div>
  );
}

export default App;
