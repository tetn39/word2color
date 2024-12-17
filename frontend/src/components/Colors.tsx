import React, { useState } from "react";
import axios from "axios";

const Colors = () => {
  const [word, setWord] = useState("");
  const [colorCodes, setColorCodes] = useState<string[]>([]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const response = await axios.get(
        `http://localhost:8000/word2color?word=${word}`
      );
      const colorCodes = response.data.color_codes;
      setColorCodes(colorCodes);
      console.log("Color codes:", colorCodes);
    } catch (error) {
      console.error("Error fetching color code:", error);
    }
  };

  return (
    <div className="max-w-lg mx-auto p-6 md:p-8 lg:p-12 bg-white rounded-lg shadow-md">
      <h1 className="text-4xl font-extrabold text-gray-800 mb-6">
        Word to Color
      </h1>
      <p className="text-lg text-gray-600 mb-8">
        単語を入力して、関連するカラーコードを生成してみましょう。
      </p>
      <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
        <label htmlFor="word" className="text-gray-700 font-medium">
          単語を入力:
        </label>
        <input
          type="text"
          id="word"
          value={word}
          onChange={(e) => setWord(e.target.value)}
          className="w-full p-3 text-gray-800 bg-gray-100 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-orange-400"
          placeholder="例: 空, 海, 森"
        />
        <button
          type="submit"
          className="w-full py-3 bg-orange-500 hover:bg-orange-600 text-white font-bold rounded-lg shadow-md transition-all duration-200"
        >
          色を生成
        </button>
      </form>
      <div className="relative w-full h-64 flex justify-center items-center mt-6">
        <div className="absolute text-center text-2xl font-bold text-gray-800">
          {word}
        </div>
        {colorCodes.map((colorCode, index) => {
          const angle = (360 / colorCodes.length) * index;
          const radius = 100; // 円の半径
          const x = Math.cos((angle * Math.PI) / 180) * radius;
          const y = Math.sin((angle * Math.PI) / 180) * radius;
          return (
            <div
              key={index}
              className="absolute w-12 h-12 rounded-full shadow-lg"
              style={{
                backgroundColor: colorCode,
                transform: `translate(${x}px, ${y}px)`,
              }}
            ></div>
          );
        })}
      </div>
    </div>
  );
};

export default Colors;
