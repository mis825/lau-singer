import React from "react";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

import "./Login.css";

function Login(props) {
  const [name, setName] = useState("");
  const [nameError, setNameError] = useState("");

  const navigate = useNavigate();

  const onFormSubmit = (e) => {
    e.preventDefault();
    setNameError("");

    if ("" === name) {
      setNameError("Please enter a name");
      return;
    }

    logIn();
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
        navigate("/draw");
      } else {
        setNameError("Name already taken");
      }
    });
  };

  return (
    <div className="Login">
      <header className="Login-header">
        <h1>Battle Draw</h1>
      </header>

      <br />
      <div className={"inputContainer"}>
        <form onSubmit={onFormSubmit}>
          <input
            value={name}
            placeholder="Enter your name"
            onChange={(ev) => setName(ev.target.value)}
            className={"inputBox"}
          />
        </form>
        <label className="errorLabel">{nameError}</label>
      </div>

      <br />
      <div className={"inputContainer"}>
        <input
          className={"inputButton"}
          type="button"
          onClick={onFormSubmit}
          value={"Enter"}
        />
      </div>
    </div>
  );
}

export default Login;
