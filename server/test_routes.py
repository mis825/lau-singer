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
        print(f'Received message in {room}: {data}\n')
        
    @sio.on('join_room_error')
    def on_join_room_error(data):
        print(f"Error while joining room: {data['error']}")

    try:
        sio.connect('http://localhost:5000')
        sio.emit('join_room', {'room': room, 'username': username})
    except Exception as e:
        print(f"Error while connecting or joining room: {e}")
        return None

    return sio  # Return the client so it can be disconnected later

def test_create_room(username):
    response = requests.post('http://localhost:5000/create-room', json={'username': username})
    if response.status_code == 201:
        print(f'{username} created room successfully')
        room_code = response.json()['room_code']
        return room_code
    else:
        print(f'Error creating room: {response.status_code}')
        return None

def test_delete_room(username, room_code):
    # username is a query parameter 
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

def test_send_message(sio, room, message):
    print(f'Sending message in {room}') # DEBUG
    sio.emit('send_message', {'room': room, 'message': message})
    print(f'Message sent') # DEBUG

    sio.sleep(2)
    # sio.disconnect()
    # print(f'Disconnected from {room}.')

if __name__ == "__main__":
    print('Testing creating a room and joining it...')
    room_1 = test_create_room('user1')
    if room_1 is not None:
        print('Room created:', room_1)
        print('user1 joining the room...')
        sio1 = test_join_room('user1', room_1)
        print('user2 joining the room...')
        sio2 = test_join_room('user2', room_1)
    print('\n')
    active_rooms = test_get_rooms()
    
    print('Testing a client joining a different room...')
    room_2 = test_create_room('user3')
    if room_2 is not None:
        print('Another room created:', room_2)
        print('user3 joining the room...')
        sio3=test_join_room('user3', room_2)
    active_rooms = test_get_rooms()
    print('\n')

    # print('Testing joining a room that does not exist...')
    # sio4 = test_join_room('user4', '123456')
    # active_rooms = test_get_rooms()
    
    print('Testing sending messages in the rooms...')
    test_send_message(sio1, room_1, 'Hi!!!!')
    test_send_message(sio2, room_1, 'Bye!!!')
    
    # print('Testing deleting rooms...')
    # # shouldn't work because user2 is not the creator of room1
    # print('User2 trying to delete room1...should fail')
    # test_delete_room('user2', room_1)
    # print('User1 deleting room1...should work')
    # test_delete_room('user1', room_1)
    # print('\n')
    # active_rooms = test_get_rooms()

