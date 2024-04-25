import React, { useEffect, useState, useRef } from "react";
// import io from "socket.io-client";
import Socket from "../../services/Socket";

import "./Chat.css";

// const socket = Socket.getSocket();


const Chat = (props) => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [shouldClear, setShouldClear] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [correctGuesses, setCorrectGuesses] = useState(0);
  const socket = Socket.getSocket();

  const messageList = useRef(null);
  const scoreList = useRef(null);

  useEffect(() => {
    console.log("scoers: ", props.scores);
  }, [props.scores]);

  useEffect(() => {
    // check for scores
    if (props.room) {
      let url = new URL(`${Socket.getServerURL()}/get_scores/${props.room}`);
      fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          props.setScores(data);
          // console.log("Scores: ", data);
        });
    }
  }, [messages]);

  useEffect(() => {
    // console.log("Game state: ", props.gameState, "  shouldClear: ", shouldClear, "countdown: ", props.countdown, "gameOver: ", gameOver);
    if (shouldClear && props.gameState === "playing" && props.countdown !== 0 && !gameOver) {
      // console.log("Clearing countdown (correct-guess): ", props.countdown);
      clearInterval(props.countdown);
      props.setCountdown(0);
      props.setTimeRemaining(0);
      if (props.host === props.name) {
        socket.emit("countdown_start", { room: props.room, duration: 60});
        // console.log("Countdown started", props.countdown);
      }
      setShouldClear(false);
    } else if (shouldClear && gameOver) {
      // console.log("Clearing countdown (gameover): ", props.countdown);
      clearInterval(props.countdown);
      props.setCountdown(0);
      props.setTimeRemaining(0);
      setShouldClear(false);
    }
  }, [shouldClear, props.gameState, gameOver, props.countdown]);

  useEffect(() => {
    if (props.name && props.loggedIn) {
      socket.emit("join_room", { username: props.name, room: props.room });

      socket.on("player_list", (players) => {
        console.log("player_list: ", players);
        props.setPlayers(players);
      });

      socket.on("switch_admin_success", (data) => {
        props.setHost(data.new_admin);
        props.setWord("");
      });

      socket.on("rotate_artist_success", (data) => {
        props.setArtist(data.new_artist);
        props.setWord("");
        props.setTimeRemaining(0);
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

      socket.on("correct_guess", (message) => {
        setMessages((messages) => [
          ...messages,
          {
            username: message.username,
            message: message.message,
            timestamp: getTime(message.timestamp),
            isGameMessage: message.isGameMessage,
          },
        ]);
        // console.log("message", message);
        if (message.startCountdown) {
          setShouldClear(true);
        }
      });

      socket.on("start_game_success", (data) => {
        props.setGameState("playing");
        setGameOver(false);
      });

      socket.on("game_over", (data) => {
        console.log("Game over");
        props.setGameState("waiting");
        props.setArtist("");
        props.setWord("");
        setShouldClear(true);
        setGameOver(true);
      });

      // socket.on("countdown", data => {
      //   socket.emit("countdown_start", { room: props.room, duration: 60 }); // start here.
      // });

      socket.on("countdown_start", (data) => {

        if (props.countdown) {
          return;
        }

        
        let timeRemaining = data.duration;
        
        const countdownInterval = setInterval(() => {
          // Update the state with the current remaining time
          props.setTimeRemaining(timeRemaining);
          
          if (timeRemaining === 0) {
            socket.emit("countdown", {
              room: props.room,
              username: props.name,
            });
            // clearInterval(countdownInterval);
            console.log("clearing countdown (countdown_start): ", countdownInterval);
            setShouldClear(true);
          } else {
            // Decrease the remaining time
            timeRemaining -= 1;
          }
        }, 1000);
        
        props.setCountdown(countdownInterval);
        // console.log("starting a new countdown", countdownInterval);
      });
      
      
      function getTime(timestamp) {
        // timestamp is in format "18:23:59"
        // we want to output time as "6:23"
        const timeParts = timestamp.split(":");
        const date = new Date();
        date.setHours(timeParts[0]);
        date.setMinutes(timeParts[1]);
        return date.toLocaleTimeString([], {
          hour: "numeric",
          minute: "2-digit",
        });
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
        socket.off("rotate_artist");
        socket.off("receive_message");
        socket.off("correct_guess");
        socket.off("start_game_success");
        socket.off("countdown_start");
        socket.off("countdown");
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

  // Hide chat form for artists
  useEffect(() => {
    if (props.artist === props.name) {
      document.querySelector(".chat-form").style.display = "none";
    } else {
      document.querySelector(".chat-form").style.display = "block";
    }
  }, [props.artist, props.name]);

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
          <div className="player-count">{props.players.length} players</div>
          {props.timeRemaining === 0 ? (
            <div className="game-countdown">Waiting for next round...</div>
          ) : (
            <div className="game-countdown">{props.timeRemaining} seconds</div>
          )}
          <div className="score-list">
            {Object.keys(props.scores).length > 0 && (
              <ul className="table">
                <li className="header">
                  <span className="player">Player</span>
                  <span className="score">Score</span>
                </li>
                {Object.entries(props.scores).map(([player, score]) => (
                  <li key={player}>
                    <span className="player">{player}</span>
                    <span className="score">{score}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <ul className="chat-messages" ref={messageList}>
            {messages.map((msg, index) => (
              <li key={index}>
                {props.host === msg.username ? (
                  <span className="chat-host">{msg.username}: </span>
                ) : msg.isGameMessage ? (
                  <span className="chat-game-message">{msg.username}: </span>
                ) : (
                  <span className="chat-username">{msg.username}: </span>
                )}
                {msg.message}
                {<span className="chat-timestamp"> {msg.timestamp}</span>}
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
