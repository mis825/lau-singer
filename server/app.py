import os 
import logging 
import random
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, send, emit, disconnect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv() 

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)
migrate = Migrate(app, db)

socketio = SocketIO(app, cors_allowed_origins="*")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
# logger.setLevel(logging.DEBUG) # uncomment to debug

# Global dictionary to store the active rooms and the clients in them
active_rooms = {}
# Global dictionary to store sid-username pairs
sid_to_username = {}
# Global dictionary to store room code-creator mapping
room_to_creator = {}

# User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # password_hash = db.Column(db.String(120))

# Room Table
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6), nullable=False, unique=True)  # Room code replaces name

# # Message Table
# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(1000), nullable=False)
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

#     user = db.relationship('User', backref=db.backref('messages', lazy=True))
#     room = db.relationship('Room', backref=db.backref('messages', lazy=True))

# Create database tables
def create_tables():
    db.create_all()
    
def generate_room_code():
    while True:
        room_code = ''.join(random.choice('0123456789') for _ in range(6))
        # use the active_rooms dictionary to check if the room code already exists
        if room_code not in active_rooms:
            return room_code
        else:
            continue # try again

# Routes
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    # password = data['password']
    # hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Check if username already exists
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "Username already taken. Please choose a different name."}), 400
    
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registered successfully."}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    # password = data['password']
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"message": "Invalid username"}), 401

    session['username'] = user.username
    return jsonify({"message": "Login successful"}), 200

@app.route('/api/get-rooms', methods=['GET'])
def get_rooms():
    return jsonify(list(active_rooms.keys())), 200

@app.route('/create-room', methods=['POST'])
def create_room():
    username = request.json['username']
    room_code = generate_room_code()
    active_rooms[room_code] = set() # add the room code to the active_rooms dictionary, with an empty set of clients
    # Store the username of the creator with the room code when the room is created
    room_to_creator[room_code] = username
    if room_code is None:
        return jsonify({"message": "Error creating room"}), 500
    return jsonify({"room_code": room_code}), 201

@app.route('/join/<room_code>', methods=['GET'])
def join_room_by_code(room_code):
    # handle the client connections here, just use the join_room function in sio
    print(active_rooms)
    # for key in active_rooms.keys():
    #     print(type(key))
    #     break
    room_code_str = str(room_code)

    if room_code_str not in active_rooms:
        return jsonify({"message": "Room not found"}), 404
    else: 
        print("Room found") # DEBUG 

    # Return a JSON response with a success message
    return jsonify({"message": f"Successfully joined room {room_code}"}), 200

@app.route('/room/<room_code>', methods=['GET'])
def room_page(room_code):
    room = Room.query.filter_by(code=room_code).first()
    if room is None:
        return jsonify({"message": "Room not found"}), 404

    # Render the room page here
    # return render_template('room.html', room=room)
    
    # placeholder for now
    return jsonify({"message": f"You are in room {room.code}"}), 200

@app.route('/room/<room_code>', methods=['DELETE'])
def delete_room(room_code):
    # Get the username from the query parameters
    username = request.args.get('username')

    # Check if the room exists in active_rooms
    if room_code not in active_rooms:
        return jsonify({"message": "Room not found"}), 404

    # Check if the current user is the creator of the room
    room_creator = get_room_creator(room_code)
    if username != room_creator:
        return jsonify({"message": "Only the creator of the room can delete it"}), 403

    # Delete the room from active_rooms
    del active_rooms[room_code]

    return jsonify({"message": f"Room {room_code} deleted successfully"}), 200

def get_current_user():
    # get the username associated with the sid
    return sid_to_username.get(request.sid)

def get_room_creator(room_code):
    # get the username of the creator associated with the room code
    return room_to_creator.get(room_code)

@socketio.on('connect')
def handle_connect():
    # Add the user to the room
    if 'room_code' in session:
        join_room(session['room_code'])
        # store the username-sid pair in the sid_to_username dictionary
        sid_to_username[request.sid] = session['username']

@socketio.on('disconnect')
def handle_disconnect():
    # iterate over a copy of the active_rooms dictionary
    #  the dictionary's keys (room codes) and values (sets of clients) are unpacked into room_code and clients
    for room_code, clients in list(active_rooms.items()):
        # check if the sid of the disconnecting client is in the set of clients for this room.
        if request.sid in clients:
            # if so, remove the sid from the set of clients.
            clients.remove(request.sid)
            # check if the set of clients is now empty
            if not clients:
                # if so, delete the room from the active_rooms dictionary
                del active_rooms[room_code]
            # break out of the loop, since a client can only be in one room at a time, and we have found the room, so no need to check the other rooms
            break

@socketio.on('join_room')
def handle_join_room(data):
    # get the room code and username from the data
    room_code = data['room']
    username = data['username']

    # check if the room exists in active_rooms
    if room_code not in active_rooms:
        emit('join_room_error', {'error': 'Room not found'}) # emit a custom event with error message to the client
        return

    join_room(room_code)
    # active_rooms[room_code].add(request.sid) # add the client to the set of clients for this room
    active_rooms[room_code].add(username) # add the username to the set of clients for this room
    send(f"{username} has joined the room: {room_code}.", to=room_code)

@socketio.on('leave_room')
def handle_leave_room(data):
    room_code = data['room']
    username = data['username']

    if room_code in active_rooms and username in active_rooms[room_code]: # request.sid 
        leave_room(room_code)
        active_rooms[room_code].remove(username)
        send(f"{username} has left the room: {room_code}.", room=room_code)

        # check if the set of clients for this room is now empty
        if not active_rooms[room_code]:
            del active_rooms[room_code]

@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    message = data['message'] 
    timestamp = datetime.now().strftime('%H:%M:%S') # get the current time
    sid = request.sid
    data['timestamp'] = timestamp
    data['sid'] = sid
    
    print(f'room: {room}') # DEBUG
    print(f'message: {message}') # DEBUG
    print(f'sid: {sid}') # DEBUG
    print(f'timestamp: {timestamp}') # DEBUG
    
    print(f'Emitting receive_message in {room}')  # DEBUG
    emit('receive_message', data, room=room)
    
@socketio.on('switch_admin')
def handle_switch_admin(data):
    room_code = data['room']
    old_admin_username = data['old_admin']
    new_admin_username = data['new_admin']

    # Check if the room exists
    if room_code not in active_rooms:
        emit('switch_admin_error', {'error': 'Room not found'})
        return

    # Check if the new admin is in the room
    if new_admin_username not in active_rooms[room_code]:
        emit('switch_admin_error', {'error': 'New admin not found in the room'})
        return
    
    # Check if the current user is the admin of the room
    if old_admin_username != room_to_creator[room_code]:
        emit('switch_admin_error', {'error': 'Only the admin can switch admin rights'})
        return

    # Switch the admin rights to the new admin
    room_to_creator[room_code] = new_admin_username
    emit('switch_admin_success', {'message': f'Admin rights for room {room_code} have been switched to {new_admin_username}'})

if __name__ == "__main__":
    with app.app_context():
        create_tables() # create the database tables if they do not exist
    socketio.run(app, host="localhost", debug=True)
