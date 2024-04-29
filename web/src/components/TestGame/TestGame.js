import React from "react";
import Canvas from "../Canvas/Canvas";
import Chat from "../Chat/Chat";
import Admin from "../Admin/Admin";

function TestGame(props) {
  return (
    <div className="Game-container">
      <Canvas width={800} height={600} />
      <Chat name={props.name} loggedIn={props.loggedIn} room={props.room} />
      <Admin name={props.name} loggedIn={props.loggedIn} room={props.room} host={props.name} />
    </div>
  );
}

export default TestGame;
