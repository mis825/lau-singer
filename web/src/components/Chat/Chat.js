import React, { useEffect, useState, memo, useRef } from "react";
import io from "socket.io-client";

import "./Chat.css";

const socket = io("http://localhost:5000"); // replace with your server address

const Chat = memo((props) => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const messageList = useRef(null);

  useEffect(() => {
    if (props.name) {
      socket.emit("join", { username: props.name, room: "304270" });
  
      socket.on("message", (message) => {
        setMessages((messages) => [
          ...messages,
          `${message.username}: ${message.msg}`,
        ]);
      });

      socket.on("leave", (message) => {
        setMessages((messages) => [
          ...messages,
          `${message.username}: ${message.msg}`,
        ]);
      });
  
      // Cleanup function
      return () => {
        // Remove the event listener
        socket.off("message");
        socket.off("leave");
        socket.emit("leave", { username: props.name, room: "304270" });
      };
    }
  }, []);   

  useEffect(() => {
    if (messageList.current) {
      messageList.current.scrollTop = messageList.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = (e) => {
    e.preventDefault();
    if (message && props.name) {
      socket.emit(
        "message",
        { username: props.name, message: message, room: "304270" },
        () => setMessage("")
      );
    }
  };

  return (
    <div className="chat-container">
      <ul className="chat-messages" ref={messageList}>
        {messages.map((msg, index) => (
          <li key={index}>{msg}</li>
        ))}
      </ul>

      {!props.name ? (
        <a href="/">Click to begin chatting</a>
      ) : (
        <form className="chat-form" onSubmit={sendMessage}>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
          <button type="submit">Send</button>
        </form>
      )}
    </div>
  );
}, (prevProps, nextProps) => {
  // Only re-render if the 'name' prop has changed
  console.log(prevProps, nextProps);
  return prevProps.name === nextProps.name; 
});


export default Chat;
