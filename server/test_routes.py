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
        print(f'{username} joined room {room}') # DEBUG
    except Exception as e:
        print(f"Error while connecting or joining room: {e}")
        return None

    return sio  # Return the client so it can be disconnected later

def test_leave_room(sio, username, room):
    print(f'{username} leaving room {room}') # DEBUG
    sio.emit('leave_room', {'room': room, 'username': username})
    print(f'{username} left room {room}') # DEBUG


def test_create_room(username):
    print(f'{username} creating room...')
    response = requests.post('http://localhost:5000/create-room', json={'username': username})
    if response.status_code == 201:
        room_code = response.json()['room_code']
        print(f'Room {room_code} created successfully by {username}')
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
    
def test_create_and_join_room(user1: str, user2: str) -> bool:
    print('Testing creating a room and joining it...')
    print('---------------------------------')
    room_1 = test_create_room(user1)
    if room_1 is not None:
        sio1 = test_join_room(user1, room_1)
        sio2 = test_join_room(user2, room_1)
        return sio1 is not None and sio2 is not None
    return False

def test_join_different_room(username: str) -> bool:
    print('Testing joining a different room...')
    print('---------------------------------')
    room_2 = test_create_room(username)
    if room_2 is not None:
        sio3 = test_join_room(username, room_2)
        return sio3 is not None
    return False

def test_join_nonexistent_room(username: str, room_code: str) -> bool:
    print('Testing joining a room that does not exist...')
    print('---------------------------------')
    sio = test_join_room(username, room_code)
    
def test_send_messages(username: str) -> bool:
    print('Testing sending messages in room...')
    print('---------------------------------')
    room_1 = test_create_room(username)
    if room_1 is not None:
        sio1 = test_join_room(username, room_1)
        test_send_message(sio1, room_1, 'Hi!!!!')
        test_send_message(sio1, room_1, 'Bye!!!')
        return True
    return False

def test_user_delete_room(user1: str,  user2: str) -> bool:
    print('Testing deleting a room...')
    print('---------------------------------')
    room1 = test_create_room(user1)
    if room1 is not None:
        sio1 = test_join_room(user1, room1)
        sio2 = test_join_room(user2, room1)
        print('user2 trying to delete room1...should fail')
        test_delete_room(user2, room1) 
        print('user1 deleting room1...should work')
        test_delete_room(user1, room1) 
        return True
    return False
    
def test_destroy_empty_rooms_if_empty(username: str) -> bool: 
    print('Testing that empty rooms will be destroyed if all users leave the room...')
    print('---------------------------------')
    
    # Create a room
    room_code = test_create_room(username)
    
    # Join the room
    sio1 = test_join_room(username, room_code)
    
    # Leave the room
    test_leave_room(sio1, username, room_code)

    # Check if the room still exists
    active_rooms = test_get_rooms()
    if room_code in active_rooms:
        print(f'Room {room_code} still exists')
        return False
    else:
        print(f'Room {room_code} has been destroyed')
        return True
          
def test_destroy_rooms_if_not_empty(user1: str, user2: str, user3: str) -> bool:
    print('Testing that empty rooms will not be destroyed if only some users leave the room...')
    print('---------------------------------')
    
    # Create a room
    room_code = test_create_room(user1)
    
    # Join the room
    sio1 = test_join_room(user1, room_code)
    sio2 = test_join_room(user2, room_code)
    sio3 = test_join_room(user3, room_code)
    
    # Leave the room
    test_leave_room(sio1, user1, room_code)
    test_leave_room(sio2, user2, room_code)
    
    # Check if the room still exists
    active_rooms = test_get_rooms()
    if room_code in active_rooms:
        print(f'Room {room_code} still exists')
        return True
    else:
        print(f'Room {room_code} has been destroyed')
        return False

if __name__ == "__main__":
    assert test_create_and_join_room(user1='user1', user2='user2') == True
    active_rooms = test_get_rooms()
    print('\n')
    
    assert test_join_different_room(username='user3') == True
    active_rooms = test_get_rooms()
    print('\n')

    assert test_join_nonexistent_room(username='user4', room_code='1234') == None
    active_rooms = test_get_rooms()
    print('\n')
    
    assert test_send_messages(username='user1') == True
    active_rooms = test_get_rooms()
    print('\n')
    
    assert test_user_delete_room(user1='user1', user2='user2') == True
    active_rooms = test_get_rooms()
    print('\n')
    
    assert test_destroy_empty_rooms_if_empty(username='user1') == True
    print('\n')
    assert test_destroy_rooms_if_not_empty(user1='user1', user2='user2', user3='user3') == True