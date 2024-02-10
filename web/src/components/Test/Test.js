import React from "react";
import { useState, useEffect } from "react";

const Test = () => {

    const [users, setUsers] = useState([]);
    const [targetUser, setTargetUser] = useState({});

  const getUser = () => {
    const data = {
      name: targetUser || "Michael",
    };

    fetch(`http://localhost:5000/api/get-user?name=${targetUser}`, {
      method: "GET",
    }).then((response) => {
        if (response.ok) {
            console.log(response);
            response.json().then((data) => {
                console.log(data);
                setUsers(data);
            });
        } else {
            console.log("Error");
        }
    });
  };

  return (
    <div>
      <h1>Test</h1>
        <input
            value={targetUser}
            placeholder="Enter a name"
            onChange={(ev) => setTargetUser(ev.target.value)}
        />
        <br />
        <button onClick={getUser}>Get Users</button>
    </div>
  );
};

export default Test;
