import os 
import logging 
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send
from flask_cors import CORS
from dotenv import load_dotenv
from db_utils import initialize_db, create_user, delete_user_name, get_user_by_id, get_user_by_name, generate_unique_room_id, create_room, delete_room, join_room, leave_room

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

@socketio.on('message')
def handle_message(message):
    logger.info("Received message: " + message)
    if message != "User connected!":
        send(message, broadcast=True)

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
    room_name = request.json.get('name', room_id)  
    max_users = request.json.get('max_users', 8)  
    response, status = create_room(room_id, room_name, max_users)
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
    response, status = join_room(user_id, room_id)
    return jsonify(response), status

@app.post("/api/leave-room")
def api_leave_room():
    user_id = request.json.get('user_id')
    room_id = request.json.get('room_id')
    if not user_id or not room_id:
        return jsonify({"message": "Missing user_id or room_id"}), 400
    response, status = leave_room(user_id, room_id)
    return jsonify(response), status

if __name__ == "__main__":
    socketio.run(app, host="localhost", debug=True)
            