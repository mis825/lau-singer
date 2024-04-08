import React from "react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Socket from "../../services/Socket";
import { delay } from "../../utils";

import "./Rooms.css";

function Rooms(props) {
  const [rooms, setRooms] = useState([0, 0, 0, 0]);
  const [roomKey, setRoomKey] = useState("");
  const [roomError, setRoomError] = useState("");
  const navigate = useNavigate();
  const socket = Socket.getSocket();

  const onButtonClick = () => {
    // setRoomError("");

    // if ("" === roomKey) {
    //   setRoomError("Please enter a room number");
    //   return;
    // }

    // if (roomKey.length < 5) {
    //   setRoomError("Please enter a 5-digit number");
    //   return;
    // }

    // if (!parseInt(roomKey)) {
    //   setRoomError("Please enter a 5-digit number");
    //   return;
    // }

    createRoom();
  };

  const createRoom = async () => {
    if (props.loggedIn) {
      fetch(`${Socket.getServerURL()}/create-room`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: props.name,
        }),
      }).then((response) => {
        if (response.ok) {
          response.json().then((data) => {
            if (data.error) {
              setRoomError(data.error);
            } else {
              props.setRoom(data.room_code);
              navigate("/game");
            }
          });
        }
      });
    }
    await delay(150);
    refreshRooms();
  };

  useEffect(() => {
    if (!props.loggedIn || !props.name) {
      navigate("/");
    }
  }, [props.loggedIn, navigate]);

  useEffect(() => {
    refreshRooms();
  }, [props.loggedIn]);

  const refreshRooms = async () => {
    if (props.loggedIn) {
      fetch(`${Socket.getServerURL()}/api/get-rooms`, {
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
  };

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
        {/* <input
          value={roomKey}
          placeholder="Enter room number"
          onChange={(ev) => setRoomKey(ev.target.value)}
          className={"inputBox"}
        />
        <label className="errorLabel">{roomError}</label> */}
        <input
          className={"inputButton"}
          type="button"
          onClick={onButtonClick}
          value={"Create Room"}
        />

        <input
          className={"inputButton"}
          type="button"
          onClick={refreshRooms}
          value={"Refresh Rooms"}
        />
      </div>
      <ul className="roomList">
        {rooms.map((room, index) => {
          return (
            <li key={index}>
              <a className="roomLink"
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
