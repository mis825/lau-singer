import React from "react";
import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Socket from "../../services/Socket";

import "./Admin.css";

const Admin = (props) => {
  const socket = Socket.getSocket();

  const clearCanvas = () => {
    socket.emit("clearCanvas", { room: props.room, name: props.name });
  };

  const deleteRoom = () => {
    // console.log("propsname: ", props.name);
    let url = new URL(`http://localhost:5000/room/${props.room}`);
    url.searchParams.append("username", props.name);

    console.log("url: ", url);

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
  }

  const getWord = () => {
    if (props.name !== props.host) return;
    
    let url = new URL(`http://localhost:5000/get_word/${props.room}`);
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
  }

  return (
    <div className="Admin-container">
      <button onClick={clearCanvas}>Clear Canvas</button>
      <button onClick={deleteRoom}>Delete Room</button>
      <button onClick={switchAdmin}>Rotate Admin</button>
      <button onClick={getWord}>Get Word</button>
    </div>
  );
};

export default Admin;
