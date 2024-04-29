import React from "react";
import { useEffect, useState, useRef } from "react";
// import { useNavigate } from "react-router-dom";
import Socket from "../../services/Socket";

import "./Admin.css";

const Admin = (props) => {
  const socket = Socket.getSocket();

  useEffect(() => {
    // Load roles
    getRoles();
    getWord();
  }, [props.artist]);

  const clearCanvas = () => {
    socket.emit("clearCanvas", { room: props.room, name: props.name });
  };

  const deleteRoom = () => {
    let url = new URL(`${Socket.getServerURL()}/room/${props.room}`);
    url.searchParams.append("username", props.name);

    fetch(url, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    }).then((response) => {
      if (response.status === 200) {
        console.log("Room deleted");
      }
    });
  };

  const switchAdmin = () => {
    socket.emit("switch_admin", { room: props.room, old_admin: props.name });
  };

  const getWord = () => {
    if (props.name !== props.artist) return;

    let url = new URL(`${Socket.getServerURL()}/get_word/${props.room}`);
    fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        props.setWord(data.word);
      });
  };

  const getRoles = () => {
    let url = new URL(`${Socket.getServerURL()}/display_roles/${props.room}`);

    fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        props.setRoles(data[props.name]);
      });
  };

  const rotateArtist = () => {
    socket.emit("rotate_artist", { room: props.room });
  };

  const startGame = () => {
    // Admin-only action
    if (props.name !== props.host) return;

    if (props.gameState === "playing") return;

    if (props.countdown) {
      clearInterval(props.countdown);
    }

    // Start the game countdown
    socket.emit("reset_game", { room: props.room });
    socket.emit("countdown_start", { room: props.room, duration: 60 });

    rotateArtist();

    socket.emit("start_game", { room: props.room, username: props.name });
  };

  return (
    <div className="Admin-container">
      {props.name === props.host ? (
        <>
          <button className="start-button" onClick={startGame}>Start Game</button>
          <button className="delete-button" onClick={deleteRoom}>Delete Room</button>
        </>
      ) : props.name === props.artist ? (
        <button className="clear-button" onClick={clearCanvas}>Clear Canvas</button>
      ) : null}
    </div>
  );
};

export default Admin;
