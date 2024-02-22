import os 
import logging 
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import random 
import socketio


load_dotenv()
app = Flask(__name__)
app.config['SECRET'] = os.getenv("SECRET_KEY")
sio = socketio.Server(cors_allowed_origins='*')  # For simplicity, allowing all origins. Adjust in production.
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

rooms = {}

def generate_room():
    """Generate a unique 6-digit room number."""
    while True:
        room_number = str(random.randint(100000, 999999))
        if room_number not in rooms:
            print(f'ROOM NUMBER GENERATED: {room_number}')
            return room_number

@sio.event
def create_room(sid, data):
    """Create a room and assign the creator as the host."""
    room_number = generate_room()
    rooms[room_number] = sid  # Assigning the SID as the host of the room
    sio.enter_room(sid, room_number)
    logger.info(f'CREATE ROOM: {room_number}')
    sio.emit('room_created', room_number, to=sid)

@sio.event
def join_room(sid, room_number):
    """Join an existing room."""
    if room_number in rooms:
        sio.enter_room(sid, room_number)
        logger.info(f'JOIN ROOM: {room_number}')
        sio.emit('join_success', room_number, to=sid)
    else:
        sio.emit('error', 'Room does not exist', to=sid)

@sio.event
def leave_room(sid, room_number):
    """Leave a room."""
    logger.info(f'LEAVE ROOM: {room_number}')
    sio.leave_room(sid, room_number)
    sio.emit('left_room', room_number, to=sid)

@sio.event
def delete_room(sid, room_number):
    """Delete a room if the requester is the host."""
    if room_number in rooms and rooms[room_number] == sid:
        del rooms[room_number]
        logger.info(f'DELETE ROOM: {room_number}')
        sio.emit('room_deleted', room_number, to=sid)
        sio.close_room(room_number)
        logger.info(f'ROOM CLOSED: {room_number}')
    else:
        sio.emit('error', 'Only the host can delete the room', to=sid)

if __name__ == '__main__':
    app.run(debug=True)

            