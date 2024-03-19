import React from "react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Socket from "../../services/Socket";
import { delay } from "../../utils";

import "./Rooms.css";

function Rooms(props) {
  const [rooms, setRooms] = useState([0, 0, 0, 0]);
  const [room, setRoom] = useState("")
  const [roomError, setRoomError] = useState("");
  const navigate = useNavigate();
  const socket = Socket.getSocket()

  const onButtonClick = () => {
    setRoomError("");

    if ("" === room) {
      setRoomError("Please enter a room number");
      return;
    }

    if (room.length < 5) {
      setRoomError("Please enter a 5-digit number")
      return;
    }

    if (!parseInt(room)) {
      setRoomError("Please enter a 5-digit number")
      return;
    }

    createRoom();
  };

  const createRoom = async () => {
    socket.emit("join_room", { username: props.name, room: room });
    await delay(150);
    refreshRooms();
  };

  useEffect(() => {
    if (!props.loggedIn || !props.name) {
      navigate("/");
    }
  }, [props.loggedIn, navigate]);

  useEffect(() => {
    refreshRooms()
  }, [props.loggedIn]);

  const refreshRooms = async () => {
    if (props.loggedIn) {
      fetch("http://localhost:5000/api/get-rooms", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }).then((response) => {
        if (response.ok) {
          response.json().then((data) => {
            setRooms(data);
          });
        }
      });
    }
  }

  if (!props.loggedIn) {
    return (
      <div className="Rooms">
        <header className="Rooms-header">
          <h1>Battle Rooms</h1>
        </header>
        <label className="errorLabel">Please log in to access the rooms</label>
      </div>
    );
  }

  return (
    <div className="Rooms">
      <header className="Rooms-header">
        <h1>Battle Rooms</h1>
      </header>
      <div className={"inputContainer"}>
        <input
          value={room}
          placeholder="Enter room number"
          onChange={(ev) => setRoom(ev.target.value)}
          className={"inputBox"}
        />
        <label className="errorLabel">{roomError}</label>
        <input
          className={"inputButton"}
          type="button"
          onClick={onButtonClick}
          value={"Enter"}
          />
      </div>
      <ul className="roomList">
        {rooms.map((room, index) => {
          return (
            <li key={index}>
              <a
                onClick={() => {
                  props.setRoom(room);
                  navigate("/game");
                }}
              >
                {room}
              </a>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default Rooms;
