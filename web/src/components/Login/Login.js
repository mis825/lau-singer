import React from "react";
import { useState } from "react";

import "./Login.css";

function Login() {
  const [name, setName] = useState("");
  const [nameError, setNameError] = useState("");

  const onButtonClick = () => {
    setNameError("");

    if ("" === name) {
      setNameError("Please enter a name");
      return;
    }
  };

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