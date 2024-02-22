import socketio
import logging
import threading

# Basic configuration for logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create two clients
sio_1 = socketio.Client()  # this is the client used for creating a unique room
sio_2 = socketio.Client()  # this is the client used for joining only the room

room_number_global = None  # Use this variable to track the room number

@sio_1.event
def connect():
    logger.info(f"sio_1 connected with SID {sio_1.sid}")
    # Create a room
    sio_1.emit('create_room', {})

@sio_1.event
def room_created(room_number):
    global room_number_global
    room_number_global = room_number  # Store the room number globally
    logger.info(f"Room created with number: {room_number}, SID: {sio_1.sid}")

# Adjust sio_2's connect event to wait for room_number_global to be set
@sio_2.event
def connect():
    logger.info(f"sio_2 connected with SID {sio_2.sid}")
    if room_number_global:
        sio_2.emit('join_room', room_number_global)

@sio_1.event
def join_success(room_number):
    logger.info(f"sio_1 successfully joined room {room_number}, SID: {sio_1.sid}")

@sio_2.event
def join_success(room_number):
    logger.info(f"sio_2 successfully joined room {room_number}, SID: {sio_2.sid}")

@sio_1.event
def disconnect():
    logger.info(f"sio_1 disconnected, SID: {sio_1.sid}")

@sio_2.event
def disconnect():
    logger.info(f"sio_2 disconnected, SID: {sio_2.sid}")

@sio_1.event
@sio_2.event
def error(msg):
    logger.error(f"Error: {msg}")

if __name__ == '__main__':
    try:
        sio_1.connect('http://localhost:5000')
        sio_2.connect('http://localhost:5000')
        # sio_1.wait()
        sio_2.wait()
    except socketio.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {e}")
