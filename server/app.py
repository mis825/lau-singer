import os 
import logging 
import random
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, send, emit
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

# User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # password_hash = db.Column(db.String(120))

# Room Table
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6), nullable=False, unique=True)  # Room code replaces name

# Message Table
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('messages', lazy=True))
    room = db.relationship('Room', backref=db.backref('messages', lazy=True))

# Create database tables
def create_tables():
    db.create_all()
    
def generate_room_code():
    while True:
        room_code = ''.join(random.choice('0123456789') for _ in range(6))
        room = Room.query.filter_by(code=room_code).first()
        if room is None:
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
    try:
        rooms = Room.query.all()
        return jsonify([room.code for room in rooms]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/join/<room_code>', methods=['GET'])
def join_room_by_code(room_code):
    room = Room.query.filter_by(code=room_code).first()
    if room is None:
        return jsonify({"message": "Room not found"}), 404

    # Store the room code in the user's session
    session['room_code'] = room.code

    # Redirect the user to the room page
    return redirect(url_for('room_page', room_code=room.code))

@app.route('/room/<room_code>', methods=['GET'])
def room_page(room_code):
    room = Room.query.filter_by(code=room_code).first()
    if room is None:
        return jsonify({"message": "Room not found"}), 404

    # Render the room page here
    # return render_template('room.html', room=room)
    
    # placeholder for now
    return jsonify({"message": f"You are in room {room.code}"}), 200

@socketio.on('connect')
def handle_connect():
    # Add the user to the room
    if 'room_code' in session:
        join_room(session['room_code'])

@socketio.on('join_room')
def handle_join_room(data):
    # get the room code and username from the data
    room_code = data['room']
    username = data['username']

    # check if the room exists
    room = Room.query.filter_by(code=room_code).first()

    if room is None:
        # the room does not exist, so create a new one
        room_code = generate_room_code() # this function will always return a unique room code
        room = Room(code=room_code)
        db.session.add(room)
        db.session.commit()

    join_room(room.code)
    send(f"{username} has joined the room: {room}.", room=room.code)

@socketio.on('leave_room')
def handle_leave_room(data):
    try:
        leave_room(data['room'])
        send(f"{session['username']} has left the room.", room=data['room'])

        # Check if the room is empty
        room = Room.query.filter_by(code=data['room']).first()
        if room and not socketio.server.rooms(data['room']):  # Check if the room is empty
            # Delete the room from the database
            db.session.delete(room)
            db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@socketio.on('send_message')
def handle_send_message(data):
    room_code = data['room']
    sid = request.sid
    # message = Message(content=data['message'], user_id=sid, room_id=room_code)
    # db.session.add(message)
    # db.session.commit()
    emit('receive_message', data, room=room_code)

if __name__ == "__main__":
    with app.app_context():
        create_tables() # create the database tables if they do not exist
    socketio.run(app, host="localhost", debug=True)
