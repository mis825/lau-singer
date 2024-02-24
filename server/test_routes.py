import requests
from socketio import Client

def test_register():
    response = requests.post('http://localhost:5000/register', data={
        'username': 'testuser'
    })
    print(response.json())

def test_login():
    response = requests.post('http://localhost:5000/login', data={
        'username': 'testuser'
    })
    print(response.json())

def test_get_rooms():
    response = requests.get('http://localhost:5000/api/get-rooms')
    print(response.json())
    
# def test_join_room():
#     response = requests.get('http://localhost:5000/join/367757')
#     print(response.status_code)
    
def test_join_room():
    sio = Client()

    @sio.event
    def connect():
        print('connection established')

    @sio.event
    def disconnect():
        print('disconnected from server')

    @sio.on('message')
    def on_message(data):
        print('message received with ', data)

    sio.connect('http://localhost:5000')
    sio.emit('join_room', {'room': 'testroom'})
    sio.wait()

if __name__ == "__main__":
    test_register()
    test_login()
    test_get_rooms()
    test_join_room()