import os 
import logging 
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
    name = db.Column(db.String(100), nullable=False, unique=True)

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

# SocketIO Events
@socketio.on('join_room')
def handle_join_room(data):
    join_room(data['room'])
    send(f"{session['username']} has joined the room.", room=data['room'])

@socketio.on('leave_room')
def handle_leave_room(data):
    leave_room(data['room'])
    send(f"{session['username']} has left the room.", room=data['room'])

@socketio.on('send_message')
def handle_send_message(data):
    room = data['room']
    message = Message(content=data['message'], user_id=session['user_id'], room_id=room)
    db.session.add(message)
    db.session.commit()
    emit('receive_message', data, room=room)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, host="localhost", debug=True)
            