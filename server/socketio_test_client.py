import socketio
import time

# Initialize the client
sio = socketio.Client()

# Define an event handler for receiving messages
@sio.on('message')
def on_message(data):
    print(data)
    
# Define an event handler for when the connection is established
@sio.on('connect')
def on_connect():
    print('Connected to the server')

# Define an event handler for when the connection is lost
@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from the server')

# Connect to the server
sio.connect('http://localhost:5000')

# Emit events to join rooms and send messages
sio.emit('join', {'username': 'TestUser1', 'room': '304270'})
time.sleep(1) 
sio.emit('message', {'room': '304270', 'username': 'TestUser1', 'message': 'Hello from TestUser1!'})
time.sleep(3) 

sio.emit('join', {'username': 'TestUser2', 'room': '304270'})
time.sleep(1) 
sio.emit('message', {'room': '304270', 'username': 'TestUser2', 'message': 'Hello from TestUser2!'})
time.sleep(3) 

sio.emit('join', {'username': 'TestUser3', 'room': '304270'})
time.sleep(1) 
sio.emit('message', {'room': '304270', 'username': 'TestUser3', 'message': 'Hello from TestUser3!'})
time.sleep(3) 

sio.emit('leave', {'username': 'TestUser1', 'room': '304270'})
time.sleep(3) 
sio.emit('leave', {'username': 'TestUser2', 'room': '304270'})
time.sleep(3) 
sio.emit('leave', {'username': 'TestUser3', 'room': '304270'})
time.sleep(3) 


sio.disconnect()