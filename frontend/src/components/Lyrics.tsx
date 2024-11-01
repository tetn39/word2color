import React, { useState } from "react";
import axios from "axios";

const Lyrics = () => {
  const [songTitle, setSongTitle] = useState("");
  const [lyrics, setLyrics] = useState([]);
  const [tokens, setTokens] = useState([]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const getLyrics = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/lyrics?title=${songTitle}`
        );
        setLyrics(response.data.lyrics);
        console.log(response.data.lyrics);
        setTokens(response.data.tokens);
        console.log(response.data.tokens);
      } catch (error) {
        console.error("Error fetching lyrics:", error);
      }
    };
    getLyrics();
  };

  return (
    <div className="max-w-md mx-auto p-4 pt-6 md:p-6 lg:p-12">
      <h1 className="text-3xl font-bold mb-4">Lyrics</h1>
      <p className="text-lg mb-6">This is the Lyrics page</p>
      <form onSubmit={handleSubmit} className="flex flex-col">
        <label className="block mb-2" htmlFor="song-title">
          Enter song title:
        </label>
        <input
          type="text"
          id="song-title"
          value={songTitle}
          onChange={(e) => setSongTitle(e.target.value)}
          className="w-full p-2 pl-10 text-sm text-gray-700"
          placeholder="Song title"
        />
        <button
          type="submit"
          className="bg-orange-500 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded"
        >
          Get Lyrics
        </button>
      </form>
      <div className="mt-6">
        <h2 className="text-2xl font-bold mb-2">Lyrics:</h2>
        <ul className="list-none mb-0">
          {Array.isArray(lyrics) ? (
            lyrics.map((line) => (
              <li key={line} className="text-lg mb-2">
                {line}
              </li>
            ))
          ) : (
            <li className="text-lg mb-2">No lyrics available</li>
          )}
        </ul>
      </div>
      <div className="mt-6">
        <h2 className="text-2xl font-bold mb-2">Tokens:</h2>
        <ul className="list-none mb-0">
          {Array.isArray(tokens) ? (
            tokens.map((token) => (
              <li key={token} className="text-lg mb-2">
                {token}
              </li>
            ))
          ) : (
            <li className="text-lg mb-2">No tokens available</li>
          )}
        </ul>
      </div>
    </div>
  );
};

export default Lyrics;
