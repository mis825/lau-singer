import React from "react";
import { useState, useEffect } from "react";

const Test = () => {

    const [users, setUsers] = useState([]);
    const [targetUser, setTargetUser] = useState({});
    const [targetUserId, setTargetUserId] = useState({});

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

  const getUserById = () => {
    const data = {
      id: targetUserId || 1,
    };

    fetch(`http://localhost:5000/api/get-user?id=${targetUserId}`, {
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
  }

  return (
    <div>
      <h1>Test</h1>
        <input
            value={targetUser}
            placeholder="Enter a name"
            onChange={(ev) => setTargetUser(ev.target.value)}
        />
        <br />
        <input
            value={targetUserId}
            placeholder="Enter a user id"
            onChange={(ev) => setTargetUserId(ev.target.value)}
        />
        <br />
        <button onClick={getUser}>Get Users</button>
        <button onClick={getUserById}>Get User By Id</button>
    </div>
  );
};

export default Test;
