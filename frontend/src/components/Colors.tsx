import React, { useState } from "react";
import axios from "axios";

const Colors = () => {
  const [word, setWord] = useState("");
  // arrayのusestate
  const [colorCodes, setColorCodes] = useState<string[]>([]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const response = await axios.get(
        `http://localhost:8000/word2img?word=${word}`
      );
      // color_codes:[#000000, #000000, #000000] のようなデータが来る
      const colorCodes = response.data.color_codes;
      setColorCodes(colorCodes);
      console.log("Color codes:", colorCodes);
    } catch (error) {
      console.error("Error fetching color code:", error);
    }
  };

  return (
    <div className="max-w-md mx-auto p-4 pt-6 md:p-6 lg:p-12">
      <h1 className="text-3xl font-bold mb-4">Word to Color</h1>
      <p className="text-lg mb-6">Enter a word to generate a color</p>
      <form onSubmit={handleSubmit} className="flex flex-col">
        <label className="block mb-2" htmlFor="word">
          Enter a word:
        </label>
        <input
          type="text"
          id="word"
          value={word}
          onChange={(e) => setWord(e.target.value)}
          className="w-full p-2 pl-10 text-sm text-gray-700"
          placeholder="Enter a word"
        />
        <button
          type="submit"
          className="bg-orange-500 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded"
        >
          Generate Color
        </button>
      </form>
      <h1>{word}</h1>
      <div className="mt-6">
        {colorCodes.map((colorCode, index) => (
          <div
            key={index}
            className="flex items-center justify-between p-4 my-2 bg-gray-100 rounded"
          >
            <div
              className="w-12 h-12 rounded"
              style={{ backgroundColor: colorCode }}
            ></div>
            <p className="text-gray-800">{colorCode}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Colors;
