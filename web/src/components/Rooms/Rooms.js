import React from "react";
import { useState } from "react";

import "./Rooms.css";

function Rooms(props) {

    // only logged in users can access the rooms

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
                <li><a href="/draw">Room 1: 0/10 players</a></li>
                <li>Room 2: 0/10 players</li>
                <li>Room 3: 0/10 players</li>
                <li>Room 4: 0/10 players</li>
            </ul>
        </div>
    );
}

export default Rooms;
