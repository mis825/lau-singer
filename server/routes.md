# Server Routes Documentation

## Create User
- **Route:** POST `/api/create-user`
- **Description:** Creates a new user.
- **Request Body:**
  - JSON Object:
    - `name`: Name of the user.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation.
  - `400`: User name not provided.

## Delete User
- **Route:** DELETE `/api/delete-user`
- **Description:** Deletes a user.
- **Request Body:**
  - JSON Object:
    - `name`: Name of the user to be deleted.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation.
  - `400`: User name not provided.

## Get User
- **Route:** GET `/api/get-user`
- **Description:** Retrieves user information.
- **Query Parameters:**
  - `name`: Name of the user (optional).
  - `id`: ID of the user (optional).
- **Response:**
  - JSON Object:
    - User information.
- **Status Codes:**
  - `200`: Successful operation.
  - `400`: User ID or name not provided.

## Create Room
- **Route:** POST `/api/create-room`
- **Description:** Creates a new room.
- **Request Body:**
  - JSON Object (Optional):
    - `name`: Name of the room (default: unique room ID).
    - `max_users`: Maximum number of users allowed in the room (default: 8).
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation.

## Delete Room
- **Route:** DELETE `/api/delete-room`
- **Description:** Deletes a room.
- **Request Body:**
  - JSON Object:
    - `room_id`: ID of the room to be deleted.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation.
  - `400`: Room ID is required.

## Join Room
- **Route:** POST `/api/join-room`
- **Description:** Adds a user to a room.
- **Request Body:**
  - JSON Object:
    - `user_id`: ID of the user to join the room.
    - `room_id`: ID of the room to join.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation.
  - `400`: Missing user_id or room_id.

## Leave Room
- **Route:** POST `/api/leave-room`
- **Description:** Removes a user from a room.
- **Request Body:**
  - JSON Object:
    - `user_id`: ID of the user to leave the room.
    - `room_id`: ID of the room to leave.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation.
  - `400`: Missing user_id or room_id.
