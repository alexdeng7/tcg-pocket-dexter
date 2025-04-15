import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import App from "./App";
import Results from "./results";
import Decks from "./decks";
import CardViewer from "./cardViewer";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/results" element={<Results />} />
        <Route path="/decks" element={<Decks />} />
        <Route path="/viewer" element={<CardViewer />} />
      </Routes>
    </Router>
  </React.StrictMode>
);
