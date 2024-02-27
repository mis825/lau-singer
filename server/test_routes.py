import requests
from socketio import Client

def test_join_room(username, room):
    sio = Client()

    @sio.event
    def connect():
        print(f'{username} connected')

    @sio.event
    def disconnect():
        print(f'{username} disconnected')

    @sio.on('message')
    def on_message(data):
        print('Message Received: ', data)

    try:
        sio.connect('http://localhost:5000')
        sio.emit('join_room', {'room': room, 'username': username})
    except Exception as e:
        print(f"Error while connecting or joining room: {e}")
        return None

    return sio  # Return the client so it can be disconnected later

def test_get_rooms():
    response = requests.get('http://localhost:5000/api/get-rooms')
    print('Active Rooms:', response.json())
    rooms = response.json()
    return rooms # Return the active rooms

def test_join_route(username, room_code):
    response = requests.get(f'http://localhost:5000/join/{room_code}')
    print(f'{username} joined room {room_code}: {response.text}')

if __name__ == "__main__":
    sio1=test_join_room('user1', 'room1')
    sio2=test_join_room('user2', 'room2')
    sio3=test_join_room('user3', 'room3')
    
    active_rooms = test_get_rooms()
    
    # More users join the rooms that the initial 3 users created
    for i, room_code in enumerate(active_rooms, 4):
        test_join_route(f'user{i}', room_code)
    
    sio1.disconnect()
    sio2.disconnect()
    sio3.disconnect()
    test_get_rooms()

