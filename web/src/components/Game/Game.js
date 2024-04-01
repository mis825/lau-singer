import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";

import "./Game.css";
// import Draw from "../Draw/Draw";
import Chat from "../Chat/Chat";
import Canvas from "../Canvas/Canvas";
import Menu from "../Canvas/Menu";
import CanvasProvider from "../../providers/CanvasProvider";
// import GameContext from "../../contexts/GameContext";
import Socket from "../../services/Socket";
import Admin from "../Admin/Admin";

const Game = (props) => {
  const navigate = useNavigate();
  const socket = Socket.getSocket();
  
  const [host, setHost] = useState("");
  const [artist, setArtist] = useState("");

  const [word, setWord] = useState("");
  const [roles, setRoles] = useState([]);

  useEffect(() => {
    if (!props.loggedIn || !props.name) {
      navigate("/");
    }
  }, [props.loggedIn, navigate]);

  // get host from /room/get-creator/<room_code>
  useEffect(() => {
    if (props.room) {
      let url = new URL(`http://localhost:5000/room/get-creator/${props.room}`);
      fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          setHost(data.creator);
        });
    }
  }, [props.room, props.name]);

  return props.name && props.loggedIn ? (
    <div className="Game-container">
      <CanvasProvider room={props.room} name={props.name} artist={artist}>
        <Menu word={word} roles={roles} artist={artist}/>
        <Canvas width={800} height={600} />
        <Chat
        name={props.name}
        loggedIn={props.loggedIn}
        room={props.room}
        socket={socket}
        host={host}
        setHost={setHost}
        word={word}
        setWord={setWord}
        artist={artist}
        setArtist={setArtist}
      />
      </CanvasProvider>
      
      <Admin
        name={props.name}
        loggedIn={props.loggedIn}
        room={props.room}
        socket={socket}
        host={host}
        setHost={setHost}
        word={word}
        setWord={setWord}
        roles={roles}
        setRoles={setRoles}
        artist={artist}
        setArtist={setArtist}
      />
    </div>
  ) : (
    <div className="Game-container"></div>
  );
};

export default Game;
