import requests
import time
from socketio import Client
from collections import defaultdict

# Global dictionary to store the current word for each room
room_words = {}
# Global dictionary to store the scores for each room
room_scores = defaultdict(lambda: defaultdict(int))
# Global dictionary to store the current score for each room
room_current_scores = defaultdict(lambda: 100)

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
        return 200
    elif response.status_code == 404:
        print(f'Room {room_code} not found')
        return 404
    else:
        print(f'Error joining room {room_code}: {response.status_code}')
        return None 
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

def test_get_word(room_code):
    print('Testing get_word...')
    response = requests.get(f'http://localhost:5000/get_word/{room_code}')
    if response.status_code == 200:
        print(f'Word for room {room_code}: {response.json()["word"]}')
        return True
    print(f'Failed to get word for room {room_code}')
    return False

def test_change_word(room_code):
    print('Testing change_word...')
    response = requests.get(f'http://localhost:5000/change_word/{room_code}')
    if response.status_code == 200:
        print(f'New word for room {room_code}: {response.json()["word"]}')
        return True
    print(f'Failed to change word for room {room_code}')
    return False

def test_assign_artist(room_code, username):
    response = requests.post(f'http://localhost:5000/assign_artist/{room_code}/{username}')
    if response.status_code == 200:
        print(f'Artist for room {room_code} assigned to {username}')
        return True
    elif response.status_code == 404:
        print(f'Room {room_code} not found')
    elif response.status_code == 403:
        print(f'User {username} not found')
    else:
        print(f'Failed to assign artist for room {room_code} to {username}')
    return False

def test_rotate_artist(room_code):
    print('Testing rotate_artist...')
    response = requests.post(f'http://localhost:5000/rotate_artist/{room_code}')
    if response.status_code == 200:
        print(f'Artist for room {room_code} rotated')
        return True
    print(f'Failed to rotate artist for room {room_code}')
    return False

def test_assign_guesser(room_code, username):
    response = requests.post(f'http://localhost:5000/assign_guesser/{room_code}/{username}')
    if response.status_code == 200:
        print(f'Guesser for room {room_code} assigned to {username}')
        return True
    elif response.status_code == 404:
        print(f'Room {room_code} not found')
    else:
        print(f'Failed to assign guesser for room {room_code} to {username}')
    return False

def test_display_roles(room_code):
    print('Testing display_roles...')
    response = requests.get(f'http://localhost:5000/display_roles/{room_code}')
    print(response.json())
    if response.status_code == 200:
        print(f'Roles for room {room_code} displayed')
        return True
    print(f'Failed to display roles for room {room_code}')
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

def test_switch_admin(old_admin, new_admin):
    # Create a room
    room_code = test_create_room(old_admin)
    test_get_rooms()
    if room_code is not None: 
        # Join the room
        sio_old_admin = test_join_room(old_admin, room_code)
        test_join_room(new_admin, room_code)
        
        @sio_old_admin.on('switch_admin_error')
        def on_switch_admin_error(data):
            print(f"Switch admin error: {data['error']}")
            
        @sio_old_admin.on('switch_admin_success')
        def on_switch_admin_success(data):
            print(data['message'])
        
        # Test if new admin can delete the room before the switch
        print(f'{new_admin} trying to delete room {room_code}...should fail')
        test_delete_room(new_admin, room_code) # Should fail
        
        # Switch the admin from old_admin to new_admin
        print(f'Switching admin rights from {old_admin} to {new_admin}...')
        # wait for the server to emit the switch_admin event
        sio_old_admin.sleep(3)
        sio_old_admin.emit('switch_admin', {'room': room_code, 'old_admin': old_admin, 'new_admin': new_admin})
        sio_old_admin.sleep(3)
        print(f'Admin switched')
        
        # Test if old admin can delete the room after the switch
        print(f'{old_admin} trying to delete room {room_code}...should fail')
        test_delete_room(old_admin, room_code) # Should fail
        
        # Test if new admin can delete the room after the switch
        print(f'{new_admin} trying to delete room {room_code}...should work')
        test_delete_room(new_admin, room_code) # Should work
             
        return True

def test_submit_correct_guess(username, room_code):
    # get the word to guess for the room
    response = requests.get(f'http://localhost:5000/get_word/{room_code}')
    word = response.json()['word']
    print(f'Word to guess for room {room_code}: {word}')
    
    # submit the correct guess
    response = requests.post(f'http://localhost:5000/submit_guess/{room_code}', json={'username': username, 'guess': word})
    print(f'Guess submitted by {username}: {word}')
    if response.status_code == 200:
        print(f'Correct guess for room {room_code} submitted by {username}')
        return True
    elif response.status_code == 404:
        print(f'Room {room_code} not found')
    else:
        print(f'Failed to submit guess for room {room_code} by {username}')
    return False

def test_submit_incorrect_guess(username, room_code):
    # get the word to guess for the room
    response = requests.get(f'http://localhost:5000/get_word/{room_code}')
    word = response.json()['word']
    print(f'Word to guess for room {room_code}: {word}')
    
    # submit the correct guess
    response = requests.post(f'http://localhost:5000/submit_guess/{room_code}', json={'username': username, 'guess': 'incorrect'})
    print(f'Guess submitted by {username}: incorrect')
    if response.status_code == 200:
        print(f'Incorrect guess for room {room_code} submitted by {username}')
        return True
    elif response.status_code == 404:
        print(f'Room {room_code} not found')
    else:
        print(f'Failed to submit guess for room {room_code} by {username}')
    return False

def test_get_scores(room_code):
    response = requests.get(f'http://localhost:5000/get_scores/{room_code}')
    if response.status_code == 200:
        print(f'Scores for room {room_code}: {response.json()}')
        return True
    print(f'Failed to get scores for room {room_code}')
    return False

if __name__ == "__main__":
    assert test_create_and_join_room(user1='user1', user2='user2') == True
    active_rooms = test_get_rooms()
    room1_code = active_rooms[0]
    sio3 = test_join_room(username='user3', room=room1_code)
    # sio4 = test_join_room(username='user4', room=room1_code)
    # sio5 = test_join_room(username='user5', room=room1_code)
    print('\n')
    
    # assert test_display_roles(room_code=room1_code) == True
    # assert test_rotate_artist(room_code=room1_code) == True
    # test_display_roles(room_code=room1_code)
    # assert test_rotate_artist(room_code=room1_code) == True
    # test_display_roles(room_code=room1_code)
      
    # assert test_assign_artist(room_code=room1_code, username='user888') == False
    # assert test_assign_artist(room_code='1234', username='user2') == False
    # assert test_assign_artist(room_code=room1_code, username='user1') == True
    
    # test_display_roles(room_code=room1_code)
    
    # assert test_get_word(room_code=room1_code) == True
    # assert test_change_word(room_code=room1_code) == True

    # print('Testing assign_guesser...')
    # assert test_assign_guesser(room_code=room1_code, username='random_user2') == True
    
    # test_display_roles(room_code=room1_code)
    
    # assert test_assign_artist(room_code='1234', username='user2') == False
    # assert test_assign_artist(room_code=room1_code, username='user888') == False
    
    # assert test_join_route(username='join_route_200', room_code=active_rooms[0]) == 200 
    # assert test_join_route(username='join_route_404', room_code='1234') == 404
    # print('\n')
    
    # assert test_join_different_room(username='user3') == True
    # active_rooms = test_get_rooms()
    # print('\n')

    # assert test_join_nonexistent_room(username='user4', room_code='1234') == None
    # active_rooms = test_get_rooms()
    # print('\n')
    
    # assert test_send_messages(username='user1') == True
    # active_rooms = test_get_rooms()
    # print('\n')
    
    # assert test_user_delete_room(user1='user1', user2='user2') == True
    # active_rooms = test_get_rooms()
    # print('\n')
    
    # assert test_destroy_empty_rooms_if_empty(username='user1') == True
    # print('\n')
    # assert test_destroy_rooms_if_not_empty(user1='user1', user2='user2', user3='user3') == True
    # print('\n')
    
    # test_switch_admin(old_admin='old_admin', new_admin='new_admin')
    # test_get_rooms()
    # print('\n')

    # room_code = test_create_room(username='user1')
    assert test_submit_correct_guess(username='user1', room_code=room1_code) == True
    assert test_submit_incorrect_guess(username='user2', room_code=room1_code) == True
    assert test_submit_correct_guess(username='user3', room_code=room1_code) == True
    assert test_submit_correct_guess(username='user2', room_code=room1_code) == True
    assert test_submit_correct_guess(username='user1', room_code=room1_code) == True
    test_get_scores(room_code=room1_code)
    


    
