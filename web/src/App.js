import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { useState } from "react";

import "./App.css";
import Login from "./components/Login/Login";
import Rooms from "./components/Rooms/Rooms";
// import Test from "./components/Test/Test";
import Game from "./components/Game/Game";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [name, setName] = useState("");
  const [room, setRoom] = useState("");

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          {/* <Route path="/" element={<Test />} /> */}
          <Route
            path="/"
            element={<Login setLoggedIn={setLoggedIn} setName={setName} />}
          />
          <Route
            path="/rooms"
            element={
              <Rooms loggedIn={loggedIn} name={name} setRoom={setRoom} />
            }
          />
          <Route
            path="/game"
            element={<Game loggedIn={loggedIn} name={name} room={room} />}
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
