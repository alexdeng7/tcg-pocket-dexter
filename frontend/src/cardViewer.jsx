import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import pokeball from "./assets/pokeball-spin.gif";
import "./index.css";

function CardViewer() {
  const [cardImages, setCardImages] = useState([]);
  const [packInfo, setPackInfo] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    const fetchData = async () => {
      try {
        await fetch(`${API_URL}/run-card-viewer`);

        const imageRes = await fetch(`${API_URL}/get-deck-cards`);
        const images = await imageRes.json();
        setCardImages(images);

        const packRes = await fetch(`${API_URL}/data/openThesePacks.csv`);
        const packText = await packRes.text();
        const rows = packText.split("\n").slice(1);
        const parsed = rows
          .map((row) => row.split(","))
          .filter((row) => row.length === 3)
          .map(([count, card, pack]) => ({ count, card, pack }));
        setPackInfo(parsed);

        setLoading(false);
      } catch (err) {
        console.error("Failed to fetch card or pack info:", err);
        setLoading(false);
      }
    };

    fetchData();
  }, [API_URL]);

  return (
    <div className="w-screen min-h-screen bg-gradient-to-br from-purple-100 via-pink-200 to-yellow-100 flex flex-col justify-center items-center text-center text-gray-800 px-4 py-12 relative overflow-hidden">
      <img
        src={pokeball}
        alt="Pokéball"
        className="w-84 h-auto animate-float glow-pokeball z-10 drop-shadow-2xl"
      />

      <h1 className="text-5xl md:text-6xl font-extrabold text-purple-700 drop-shadow-lg animate-pulse mb-10 font-pokemon">
        Your Final Decklist!
      </h1>

      {loading ? (
        <p className="text-lg animate-pulse text-gray-700">
          Preparing your deck...
        </p>
      ) : (
        <>
          <div className="mb-12 w-full max-w-6xl">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Your Deck</h2>
            <div className="grid grid-cols-5 gap-[2px] px-1">
              {cardImages.map((img, idx) => (
                <img
                  key={idx}
                  src={`${API_URL}/topDeckCards/${img}`}
                  alt={`Card ${idx + 1}`}
                  className="rounded-sm shadow-sm w-full h-auto hover:scale-105 transition-transform duration-200"
                />
              ))}
            </div>
          </div>

          <div className="w-full max-w-3xl bg-white/50 backdrop-blur-md p-6 md:p-8 rounded-3xl shadow-xl border border-white/30">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Missing Cards? <br />
              Here Are The Packs to Open
            </h2>
            <ul className="text-left space-y-2 text-sm md:text-base">
              {packInfo.map(({ count, card, pack }, idx) => (
                <li key={idx} className="text-gray-800">
                  <strong>{count}x</strong>{" "}
                  <span className="italic">{card}</span> →{" "}
                  <span className="font-semibold">{pack}</span>
                </li>
              ))}
            </ul>
          </div>
        </>
      )}

      <div className="mt-10 flex flex-col sm:flex-row gap-4">
        <button
          onClick={() => navigate(-1)}
          className="bg-gray-300 hover:bg-gray-400 text-gray-800 text-sm font-medium py-1.5 px-6 rounded-full transition shadow"
        >
          Back To Decks
        </button>
        <button
          onClick={() => navigate("/")}
          className="bg-purple-500 hover:bg-purple-600 text-white text-sm font-medium py-1.5 px-6 rounded-full transition shadow"
        >
          Restart Process
        </button>
      </div>

      <p className="mt-6 text-sm text-gray-600 italic z-10">
        Built by Alex Deng
      </p>

      <div className="absolute top-[-50px] left-[-50px] w-72 h-72 bg-yellow-300 opacity-30 rounded-full blur-3xl animate-spin-slow z-0" />
      <div className="absolute bottom-[-50px] right-[-50px] w-72 h-72 bg-purple-200 opacity-30 rounded-full blur-3xl animate-pulse z-0" />
    </div>
  );
}

export default CardViewer;
