import os 
import logging 
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, send
from flask_cors import CORS
from dotenv import load_dotenv
from db_utils import create_user, delete_user_name, get_user, initialize_db, create_room, generate_unique_room_id

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

@app.route("/")
def index(): 
    # landing page for now? 
    logger.info("Accessed index page.")
    return render_template("index.html") 

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
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"message": "User name not provided"}), 400
    response, status = get_user(data['name'])
    return jsonify(response), status

@app.post("/api/create-room")
def api_create_room():
    room_id = generate_unique_room_id()
    room_name = request.json.get('name', 'Default Room Name')  # Example: Use a default name or take it from request
    max_users = request.json.get('max_users', 10)  # Example: Default max users to 10
    response, status = create_room(room_id, room_name, max_users)
    return jsonify(response), status


if __name__ == "__main__":
    socketio.run(app, host="localhost", debug=True)
            