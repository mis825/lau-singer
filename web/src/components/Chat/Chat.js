import React, { useEffect, useState, useRef } from "react";
// import io from "socket.io-client";
import Socket from "../../services/Socket";

import "./Chat.css";

// const socket = Socket.getSocket();

// console.log("socket", socket);

const Chat = (props) => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const socket = Socket.getSocket();

  const messageList = useRef(null);

  useEffect(() => {
    if (props.name && props.loggedIn) {
      socket.emit("join_room", { username: props.name, room: props.room });

    socket.on("switch_admin_success", (data) => {
      props.setHost(data.new_admin);
      props.setWord("");
    });

    socket.on("rotate_artist_success", (data) => {
      props.setArtist(data.new_artist);
    });
    
      socket.on("receive_message", (message) => {
        setMessages((messages) => [
          ...messages,
          {
            username: message.username,
            message: message.message,
            timestamp: getTime(message.timestamp),
          },
        ]);
      });

      function getTime(timestamp) {
        // timestamp is in format "18:23:59"
        // we want to output time as "6:23"
        const timeParts = timestamp.split(":");
        const date = new Date();
        date.setHours(timeParts[0]);
        date.setMinutes(timeParts[1]);
        return date.toLocaleTimeString([], { hour: "numeric", minute: "2-digit"});
      }

      socket.on("leave_room", (message) => {
        setMessages((messages) => [
          ...messages,
          { username: message.username, message: message.msg },
        ]);
      });

      // Cleanup function
      return () => {
        socket.off("message");
        socket.off("leave_room");
        socket.off("switch_admin_success");
        socket.emit("leave_room", { username: props.name, room: props.room });
      };
    }
  }, [props.name, props.loggedIn, props.room]);

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
        { username: props.name, message: message, room: props.room },
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
          <div className="chat-header">Room {props.room}</div>
          <ul className="chat-messages" ref={messageList}>
            {messages.map((msg, index) => (
              <li key={index}>
                {/* <div className="chat-host-message"> */}
                {props.host === msg.username ? (
                  <span className="chat-host">{msg.username}: </span>
                ) : (
                  <span className="chat-username">{msg.username}: </span>
                )}
                {msg.message}
                {<span className="chat-timestamp">  {msg.timestamp}</span>}
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
