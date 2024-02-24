import os 
import logging 
import random
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, jsonify, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv() 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)
socketio = SocketIO(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
# logger.setLevel(logging.DEBUG) # uncomment to debug

# User Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

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

# Routes
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registered successfully."}), 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid username or password"}), 401

    session['username'] = user.username
    return jsonify({"message": "Login successful"}), 200

@app.route('/join/<room_code>', methods=['GET'])
def join_room_by_code(room_code):
    room = Room.query.filter_by(code=room_code).first()
    if room is None:
        return jsonify({"message": "Room not found"}), 404

    # add the user to the room
    join_room(room.code)

    # redirect the user to the room page
    return redirect(url_for('room_page', room_code=room.code))

@app.route('/room/<room_code>', methods=['GET'])
def room_page(room_code):
    room = Room.query.filter_by(code=room_code).first()
    if room is None:
        return jsonify({"message": "Room not found"}), 404

    # Render the room page here
    # return render_template('room.html', room=room)

@socketio.on('join_room')
def handle_join_room(data):
    # get the room code from the data
    room_code = data['room']
    # check if the room exists
    room = Room.query.filter_by(code=room_code).first()

    if room is None:
        # the room does not exist, so create a new one
        room_code = generate_room_code()
        room = Room(code=room_code)
        db.session.add(room)
        db.session.commit()

    join_room(room.code)
    send(f"{session['username']} has joined the room.", room=room.code)

@socketio.on('leave_room')
def handle_leave_room(data):
    leave_room(data['room'])
    send(f"{session['username']} has left the room.", room=data['room'])

@socketio.on('send_message')
def handle_send_message(data):
    room_code = data['room']
    message = Message(content=data['message'], user_id=session['user_id'], room_id=room_code)
    db.session.add(message)
    db.session.commit()
    emit('receive_message', data, room=room_code)
    
def generate_room_code():
    while True:
        room_code = ''.join(random.choice('0123456789') for _ in range(6))
        room = Room.query.filter_by(code=room_code).first()
        if room is None:
            return room_code

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, host="localhost", debug=True)
            