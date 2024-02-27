import React, { useEffect, useState, useRef } from "react";
import io from "socket.io-client";

import "./Chat.css";

const socket = io("http://localhost:5000");

const Chat = (props) => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const messageList = useRef(null);

  useEffect(() => {
    if (props.name && props.loggedIn) {
      socket.emit("join_room", { username: props.name, room: props.room });

      socket.on("receive_message", (message) => {
        setMessages((messages) => [
          ...messages,
          { username: message.username, message: message.msg },
        ]);
      });

      socket.on("leave", (message) => {
        setMessages((messages) => [
          ...messages,
          { username: message.username, message: message.msg },
        ]);
      });

      // Cleanup function
      return () => {
        socket.off("message");
        socket.off("leave");
        socket.emit("leave", { username: props.name, room: "304270" });
      };
    }
  }, []);

  // Autoscroll
  useEffect(() => {
    if (messageList.current) {
      messageList.current.scrollTop = messageList.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = (e) => {
    e.preventDefault();
    if (message && props.name && props.loggedIn) {
      socket.emit(
        "send_message",
        { username: props.name, msg: message, room: props.room },
        () => setMessage("")
      );
    }
  };

  return (
    <div className="chat-container">
      {!props.name || !props.loggedIn ? (
        <a href="/">Log in to begin chatting</a>
      ) : (
        <div>
          <h3>Room {props.room}</h3>
          <ul className="chat-messages" ref={messageList}>
            {messages.map((msg, index) => (
              <li key={index}>
                <span className="chat-username">{msg.username}: </span>
                {msg.message}
              </li>
            ))}
          </ul>

          <form className="chat-form" onSubmit={sendMessage}>
            <input
              type="text"
              value={message}
              placeholder="Send a message"
              onChange={(e) => setMessage(e.target.value)}
            />
            <button type="submit">Chat</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default Chat;
