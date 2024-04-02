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

## Create Room
- **Route:** POST `/create_room`
- **Description:** Creates a new room.
- **Request Body:**
  - JSON Object:
    - `username`: Username of the user creating the room.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `201`: Successful operation, room created.
  - `400`: Room already exists.

## Join Room by Code
- **Route:** POST `/join_room_by_code`
- **Description:** Joins a room identified by its code.
- **Request Body:**
  - JSON Object:
    - `username`: Username of the user joining the room.
    - `room_code`: Code of the room to join.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation, room joined.
  - `404`: Room not found.

## Room Page
- **Route:** GET `/room_page/<room_code>`
- **Description:** Gets information about a room identified by its code.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation.
  - `404`: Room not found.

## Delete Room
- **Route:** DELETE `/delete_room/<room_code>`
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

## Get Word
- **Route:** GET `/get_word/<room_code>`
- **Description:** Gets the current word for a room identified by its code.
- **Response:**
  - JSON Object:
    - `word`: Current word.
- **Status Codes:**
  - `200`: Successful operation.
  - `404`: Room not found.

## Change Word
- **Route:** POST `/change_word/<room_code>`
- **Description:** Changes the current word for a room identified by its code.
- **Request Body:**
  - JSON Object:
    - `word`: New word.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation, word changed.
  - `404`: Room not found.

## Assign Artist
- **Route:** POST `/assign_artist/<room_code>`
- **Description:** Assigns the artist role to a user in a room identified by its code.
- **Request Body:**
  - JSON Object:
    - `username`: Username of the user to assign the artist role.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation, artist assigned.
  - `404`: Room not found.

## Rotate Artist
- **Route:** POST `/rotate_artist/<room_code>`
- **Description:** Rotates the artist in a room identified by its code.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation, artist rotated.
  - `404`: Room not found.

## Assign Guesser
- **Route:** POST `/assign_guesser/<room_code>`
- **Description:** Assigns the guesser role to a user in a room identified by its code.
- **Request Body:**
  - JSON Object:
    - `username`: Username of the user to assign the guesser role.
- **Response:**
  - JSON Object:
    - `message`: Success or error message.
- **Status Codes:**
  - `200`: Successful operation, guesser assigned.
  - `404`: Room not found.

## Display Roles
- **Route:** GET `/display_roles/<room_code>`
- **Description:** Displays the roles of all users in a room identified by its code.
- **Response:**
  - JSON Object:
    - Each key is a username and each value is a list of roles.
- **Status Codes:**
  - `200`: Successful operation, roles displayed.
  - `404`: Room not found.