import React from "react";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

import "./Login.css";

function Login(props) {
  const [name, setName] = useState("");
  const [nameError, setNameError] = useState("");

  const navigate = useNavigate();

  const onButtonClick = () => {
    setNameError("");

    if ("" === name) {
      setNameError("Please enter a name");
      return;
    }

    logIn()

  };

  const logIn = () => {
    const data = {
      name: name,
    };

    fetch("http://localhost:5000/api/create-user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }).then((response) => {
      if (response.ok) {
        props.setLoggedIn(true);
        props.setName(name);
        navigate("/rooms")
      } else {
        setNameError("Name already taken");
      }
    });
  }

  return (
    <div className="Login">
      <header className="Login-header">
        <h1>Battle Draw</h1>
      </header>

      <br />
      <div className={"inputContainer"}>
        <input
          value={name}
          placeholder="Enter your name"
          onChange={(ev) => setName(ev.target.value)}
          className={"inputBox"}
        />
        <label className="errorLabel">{nameError}</label>
      </div>

      <br />
      <div className={"inputContainer"}>
        <input
          className={"inputButton"}
          type="button"
          onClick={onButtonClick}
          value={"Enter"}
        />
      </div>
    </div>
  );
}

export default Login;
