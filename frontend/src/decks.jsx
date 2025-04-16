import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Papa from "papaparse";
import pokeball from "./assets/pokeball-spin.gif";
import "./index.css";

function Decks() {
  const [decks, setDecks] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    fetch(`${API_URL}/match-decks`)
      .then(() => fetch(`${API_URL}/data/decksMatched.csv`))
      .then((res) => res.text())
      .then((csvText) => {
        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          complete: (result) => {
            setDecks(result.data.slice(0, 5));
            setLoading(false);
          },
        });
      })
      .catch((err) => {
        console.error("Error fetching matched decks:", err);
        setLoading(false);
      });
  }, [API_URL]);

  const renderTags = (text) => {
    if (!text) return null;
    return text.split(",").map((item, idx) => (
      <span
        key={idx}
        className="inline-block bg-indigo-200 text-indigo-800 text-xs font-medium mr-1 mb-1 px-2 py-1 rounded-full"
      >
        {item.trim()}
      </span>
    ));
  };

  const handleDeckSelect = async (index) => {
    try {
      await fetch(`${API_URL}/select-deck`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index }),
      });

      navigate("/viewer");
    } catch (err) {
      console.error("Failed to select deck:", err);
    }
  };

  return (
    <div className="w-screen min-h-screen bg-gradient-to-br from-blue-100 via-indigo-200 to-purple-300 flex flex-col justify-center items-center text-center text-gray-800 px-4 py-12 relative overflow-hidden">
      <img
        src={pokeball}
        alt="Pokéball"
        className="w-84 h-auto animate-float glow-pokeball z-10 drop-shadow-2xl"
      />

      <h1 className="text-5xl md:text-6xl font-extrabold text-indigo-700 drop-shadow-lg animate-pulse mb-8 font-pokemon">
        The Current Best Deck(s)
      </h1>

      <div className="bg-white/50 backdrop-blur-md p-6 md:p-10 max-w-5xl w-full rounded-3xl shadow-xl overflow-x-auto border border-white/30">
        {loading ? (
          <p className="text-lg animate-pulse">
            Searching database for the best deck(s)...
          </p>
        ) : decks.length === 0 ? (
          <p className="text-lg">No decks matched your card</p>
        ) : (
          <table className="min-w-full text-left border-separate border-spacing-y-4">
            <thead>
              <tr className="text-indigo-900 text-sm">
                <th className="px-4 pb-2">Pokémon</th>
                <th className="px-4 pb-2">Trainers</th>
                <th className="px-4 pb-2">Winrate</th>
              </tr>
            </thead>
            <tbody>
              {decks.map((deck, idx) => (
                <tr
                  key={idx}
                  className="bg-white bg-opacity-60 hover:bg-opacity-80 rounded-lg shadow transition duration-200"
                >
                  <td className="px-4 py-4 align-top">
                    <div className="flex flex-wrap">
                      {renderTags(deck.pokemon)}
                    </div>
                  </td>
                  <td className="px-4 py-4 align-top">
                    <div className="flex flex-wrap">
                      {renderTags(deck.trainers)}
                    </div>
                  </td>
                  <td className="px-4 py-4 align-top font-semibold text-indigo-700">
                    {(parseFloat(deck.winrate) * 100).toFixed(1)}%
                    <br />
                    <button
                      className="mt-2 bg-indigo-500 hover:bg-indigo-600 text-white text-xs px-3 py-1 rounded-full"
                      onClick={() => handleDeckSelect(idx)}
                    >
                      Select
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        <div className="flex flex-col sm:flex-row justify-center gap-4 mt-10">
          <button
            onClick={() => navigate("/viewer")}
            className="bg-purple-500 hover:bg-purple-600 text-white text-md font-semibold py-2 px-6 rounded-full shadow transition duration-300"
          >
            Show Me The Full Set!
          </button>
          <button
            onClick={() => navigate("/")}
            className="bg-indigo-500 hover:bg-indigo-600 text-white text-md font-semibold py-2 px-6 rounded-full shadow transition duration-300"
          >
            Restart Process
          </button>
        </div>
      </div>

      <p className="mt-10 text-sm text-gray-600 italic z-10">
        Built by Alex Deng
      </p>

      <div className="absolute top-[-50px] left-[-50px] w-72 h-72 bg-purple-300 opacity-30 rounded-full blur-3xl animate-spin-slow z-0" />
      <div className="absolute bottom-[-50px] right-[-50px] w-72 h-72 bg-blue-300 opacity-30 rounded-full blur-3xl animate-pulse z-0" />
    </div>
  );
}

export default Decks;
