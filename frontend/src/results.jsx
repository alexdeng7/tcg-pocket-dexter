import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import pokeball from "./assets/pokeball-spin.gif";
import "./index.css";

function Results() {
  const navigate = useNavigate();
  const [matchedCard, setMatchedCard] = useState(null);

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    fetch(`${API_URL}/matched-card`)
      .then((res) => res.json())
      .then((data) => setMatchedCard(data))
      .catch((err) => console.error("Error fetching matched card", err));
  }, [API_URL]);

  const cardName = matchedCard?.matched_card?.replace(".webp", "") || "";
  const cardImageURL = matchedCard
    ? `${API_URL}/croppedCards/${matchedCard.cropped_card}`
    : "";

  return (
    <div className="w-screen min-h-screen bg-gradient-to-br from-yellow-100 via-red-200 to-pink-300 flex flex-col justify-center items-center text-center text-gray-800 px-4 py-12 relative overflow-hidden">
      <img
        src={pokeball}
        alt="Pokéball"
        className="w-84 h-auto animate-float glow-pokeball z-10 drop-shadow-2xl"
      />

      <h1 className="text-5xl md:text-6xl font-extrabold text-red-600 drop-shadow-lg animate-pulse mb-8 font-pokemon">
        Your Card Analysis Is Ready!
      </h1>

      <div className="bg-white/50 backdrop-blur-md shadow-xl rounded-3xl p-8 md:p-10 max-w-xl w-full border border-white/30 text-center">
        <p className="text-lg md:text-xl text-gray-800 mb-4">
          Your screenshot has been successfully processed.
        </p>

        {matchedCard && (
          <>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              Is this your card?
            </h2>
            <img
              src={cardImageURL}
              alt="Detected card"
              className="mx-auto rounded-xl shadow-lg w-48"
            />
            <p className="text-md font-medium text-gray-700 mt-3 italic">
              {cardName}
            </p>

            <div className="flex justify-center gap-4 mt-6">
              <button
                onClick={() => navigate("/")}
                className="bg-gray-400 hover:bg-gray-500 text-white font-semibold py-2 px-6 rounded-full shadow transition duration-300"
              >
                Restart Process
              </button>
              <button
                onClick={() => navigate("/decks")}
                className="bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-6 rounded-full shadow transition duration-300"
              >
                Yes, show best deck(s)!
              </button>
            </div>
          </>
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

export default Results;
