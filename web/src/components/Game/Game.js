import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";

import "./Game.css";
import Draw from "../Draw/Draw";
import Chat from "../Chat/Chat";

const Game = (props) => {
  const navigate = useNavigate();

  useEffect(() => {
    if (!props.loggedIn || !props.name) {
      navigate("/");
    }
  }, [props.loggedIn, navigate]);

  return props.name && props.loggedIn ? (
    <div className="Game-container">
      <Draw />
      <Chat name={props.name} loggedIn={props.loggedIn} room={props.room} />
    </div>
  ) : (
    <div className="Game-container"></div>
  );
};

export default Game;
