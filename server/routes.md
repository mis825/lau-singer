# API Documentation

## Register User
- **Route:** POST `/register`
- **Description:** Registers a new user.
- **Request Body:**
  - JSON Object:
    - `username`: Username of the user.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `201`: Successful operation, user registered.
  - `400`: Username already taken.

## Login User
- **Route:** POST `/login`
- **Description:** Logs in a user.
- **Request Body:**
  - JSON Object:
    - `username`: Username of the user.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation, user logged in.
  - `401`: Invalid username.

## Get Rooms
- **Route:** GET `/api/get-rooms`
- **Description:** Gets a list of active rooms.
- **Response:**
  - JSON Array:
    - List of room codes.
- **Status Codes:**
  - `200`: Successful operation.

## Join Room
- **Route:** GET `/join/<room_code>`
- **Description:** Joins a room identified by its code.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation, room joined.
  - `404`: Room not found.

## Room Page
- **Route:** GET `/room/<room_code>`
- **Description:** Gets information about a room identified by its code.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation.
  - `404`: Room not found.

## Delete Room
- **Route:** DELETE `/room/<room_code>`
- **Description:** Deletes a room identified by its code.
- **Query Parameters:**
  - `username`: Username of the user attempting to delete the room.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation, room deleted.
  - `403`: Unauthorized operation, only the creator of the room can delete it.
  - `404`: Room not found.