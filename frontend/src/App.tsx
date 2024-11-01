import React from "react";
import { Link } from "react-router-dom";

const App = () => {
  return (
    <header className="h-40 bg-zinc-200 pt-2">
      <ul className="flex justify-around bg-zinc-200 text-center">
        <li className="inline-block w-32 text-center hover:border hover:border-zinc-400">
          <Link to="/" className="block leading-10">
            Home
          </Link>
        </li>
        <li className="inline-block w-32 text-center hover:border hover:border-zinc-400">
          <Link to="/lyrics" className="block leading-10">
            Lyrics
          </Link>
        </li>
        <li className="inline-block w-32 text-center hover:border hover:border-zinc-400">
          <Link to="/colors" className="block leading-10">
            Colors
          </Link>
        </li>
      </ul>
    </header>
  );
};

export default App;
