import React from "react";
import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import Socket from "../../services/Socket";

import "./Admin.css";

const Admin = (props) => {
  // allow the admin to clear the canvas, delete the room
  const socket = Socket.getSocket();

  const clearCanvas = () => {
    socket.emit("clearCanvas", { room: props.room });
  };

  /**
     * @app.route('/room/<room_code>', methods=['DELETE'])
def delete_room(room_code):
    # Get the username from the query parameters
    username = request.args.get('username')

    # Check if the room exists in active_rooms

     */
const deleteRoom = () => {
        console.log("propsname: ", props.name);
        let url = new URL(`http://localhost:5000/room/${props.room}`);
        url.searchParams.append('username', props.name);

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

  return (
    <div className="Admin-container">
      <button onClick={clearCanvas}>Clear Canvas</button>
      <button onClick={deleteRoom}>Delete Room</button>
    </div>
  );
};

export default Admin;
