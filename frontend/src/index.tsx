import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./components/Home";
import Lyrics from "./components/Lyrics";
import Colors from "./components/Colors";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/lyrics" element={<Lyrics />} />
        <Route path="/colors" element={<Colors />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);
