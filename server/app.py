import os 
import logging 
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send
from flask_socketio import emit, join_room, leave_room, close_room, rooms, disconnect
from flask_cors import CORS
from dotenv import load_dotenv
from db_utils import initialize_db, create_user, delete_user_name, get_user_by_id, get_user_by_name, generate_unique_room_id, create_room, delete_room, join_room as db_join_room, leave_room as db_leave_room

load_dotenv()
app = Flask(__name__)
app.config['SECRET'] = os.getenv("SECRET_KEY")
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

# initialize our database
initialize_db()

# SocketIO event for handling a new user connection
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    
# SocketIO event for joining a room
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('message', {'msg': f"{username} has entered the room.", 'username': 'System'}, to=room)
    
# SocketIO event for leaving a room
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('message', {'msg': f"{username} has left the room.", 'username': 'System'}, to=room)
    
# SocketIO event for sending a message to a room
@socketio.on('message')
def handle_message(data):
    username = data.get('username', 'Unknown')  # Optional: Handle username if included
    room = data['room']
    message = data['message']
    
    logger.info(f"Message received in room {room} from {username}: {message}")
    
    # emit the message with the username: message
    emit('message', {'msg': message, 'username': username}, to=room)

@app.post("/api/create-user")
def api_create_user():
    # parses the json into a dictionary 
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"message": "User name not provided"}), 400
    response, status = create_user(data['name'])
    return jsonify(response), status

@app.delete("/api/delete-user")
def api_delete_user():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"message": "User name not provided"}), 400
    response, status = delete_user_name(data['name'])
    return jsonify(response), status

@app.get("/api/get-user")
def api_get_user():
    name = request.args.get('name')
    id = request.args.get('id')
    if not id and not name:
        return jsonify({"message": "User ID or name not provided"}), 400
    if id:
        response, status = get_user_by_id(id=id)
    else:
        response, status = get_user_by_name(name=name)
    return jsonify(response), status

@app.post("/api/create-room")
def api_create_room():
    room_id = generate_unique_room_id()
    # default room name, max_users = room_id, 8 
    room_name = room_id
    max_users = 8
    data = request.get_json()
    if data:
        room_name = data.get('name', room_id)
        max_users = data.get('max_users', 8)
    response, status = create_room(room_name, max_users)
    return jsonify(response), status

@app.delete("/api/delete-room")
def api_delete_room():
    room_id = request.json.get('room_id')
    if not room_id:
        return jsonify({"message": "Room ID is required"}), 400
    response, status = delete_room(room_id)
    return jsonify(response), status

@app.post("/api/join-room")
def api_join_room():
    user_id = request.json.get('user_id')
    room_id = request.json.get('room_id')
    if not user_id or not room_id:
        return jsonify({"message": "Missing user_id or room_id"}), 400
    response, status = db_join_room(user_id, room_id)
    return jsonify(response), status

@app.post("/api/leave-room")
def api_leave_room():
    user_id = request.json.get('user_id')
    room_id = request.json.get('room_id')
    if not user_id or not room_id:
        return jsonify({"message": "Missing user_id or room_id"}), 400
    response, status = db_leave_room(user_id, room_id)
    return jsonify(response), status

if __name__ == "__main__":
    socketio.run(app, host="localhost", debug=True)
            