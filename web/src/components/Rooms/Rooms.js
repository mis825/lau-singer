import React from "react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import "./Rooms.css";

function Rooms(props) {
  const [rooms, setRooms] = useState([0, 0, 0, 0]);
  const navigate = useNavigate();

  useEffect(() => {
    if (!props.loggedIn || !props.name) {
      navigate("/");
    }
  }, [props.loggedIn, navigate]);

  useEffect(() => {
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
  }, [props.loggedIn]);

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
