import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";

import "./Game.css";
// import Draw from "../Draw/Draw";
import Chat from "../Chat/Chat";
import Canvas from "../Canvas/Canvas";
import CanvasProvider from "../../providers/CanvasProvider";
// import GameContext from "../../contexts/GameContext";
import Socket from "../../services/Socket";

const Game = (props) => {
  const navigate = useNavigate();
  const socket = Socket.getSocket();

  useEffect(() => {
    if (!props.loggedIn || !props.name) {
      navigate("/");
    }
  }, [props.loggedIn, navigate]);

  return props.name && props.loggedIn ? (
    <div className="Game-container">
      <CanvasProvider>
          <Canvas width={800} height={600} />
      </CanvasProvider>
      <Chat name={props.name} loggedIn={props.loggedIn} room={props.room} socket={socket} />
    </div>
  ) : (
    <div className="Game-container"></div>
  );
};

export default Game;
