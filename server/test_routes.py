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

    @sio.on('receive_message')
    def on_receive_message(data, room=room):
        print('Received data: ', data)
        print('Room: ', room)
        message = data['message']
        print(f"Received message: {message}")

    try:
        sio.connect('http://localhost:5000')
        sio.emit('join_room', {'room': room, 'username': username})
    except Exception as e:
        print(f"Error while connecting or joining room: {e}")
        return None

    return sio  # Return the client so it can be disconnected later

def test_delete_room(username, room_code):
    response = requests.delete(f'http://localhost:5000/room/{room_code}?username={username}')
    if response.status_code == 200:
        print(f'{username} deleted room {room_code} successfully')
    elif response.status_code == 404:
        print(f'Room {room_code} not found')
    elif response.status_code == 403:
        print(f'Only the creator of the room can delete it')
    else:
        print(f'Error deleting room {room_code}: {response.status_code}')

def test_get_rooms():
    response = requests.get('http://localhost:5000/api/get-rooms')
    print('Active Rooms:', response.json())
    rooms = response.json()
    return rooms # return the active rooms list

def test_join_route(username, room_code):
    response = requests.get(f'http://localhost:5000/join/{room_code}')
    if response.status_code == 200:
        print(f'{username} joined room {room_code}')
    elif response.status_code == 404:
        print(f'Room {room_code} not found')
    else:
        print(f'Error joining room {room_code}: {response.status_code}')

def test_send_message(sio, room):
    print(f'Sending message in {room}')
    sio.emit('send_message', { 'room': room, 'message': 'Hello, world!' })
    print(f'Message sent')

    sio.sleep(5)
    sio.disconnect()

    print(f'Disconnected from {room}.')

if __name__ == "__main__":
    sio1=test_join_room('user1', 'room1')
    active_rooms = test_get_rooms()
    first_room_code = active_rooms[0]
    print('First room code:', first_room_code) # DEBUG
    sio2=test_join_room('user2', first_room_code)
    # sio3=test_join_room('user3', 'room3')
    # sio4=test_join_room('user4', 'room4')
    
    # More users join the rooms that the initial 3 users created
    for i, room_code in enumerate(active_rooms, 5):
        test_join_route(f'user{i}', room_code)
    
    # sio1.disconnect()
    # sio2.disconnect()
    # sio3.disconnect()
    test_get_rooms()
    # test_send_message(sio1, 'room1')
    
    # shouldn't work because user2 is not the creator of room1
    test_delete_room('user2', first_room_code)
    test_delete_room('user1', first_room_code)

    test_get_rooms()

