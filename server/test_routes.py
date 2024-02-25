import requests
from socketio import Client
from app import app, socketio, db
from app.models import Message

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
    
def test_join_room():
    sio = Client()

    @sio.event
    def connect():
        print('Connection Established')

    @sio.event
    def disconnect():
        print('Disconnected From Server')

    @sio.on('message')
    def on_message(data):
        print('Message Received: ', data)

    sio.connect('http://localhost:5000')
    sio.emit('join_room', {'room': 'testroom', 'username': 'testuser'})
    sio.wait()

def test_leave_room():
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
    sio.emit('join_room', {'room': 'testroom', 'username': 'testuser'})
    sio.emit('leave_room', {'room': 'testroom', 'username': 'testuser'})
    sio.wait()

# def test_send_message(app, socketio, db):
#     # Create a test client
#     client = socketio.test_client(app)

#     # Define the test data
#     test_data = {'room': 'test_room', 'message': 'test_message'}

#     # Emit the 'send_message' event with the test data
#     client.emit('send_message', test_data)

#     # Receive the response
#     received = client.get_received()

#     # Check that the response contains the 'receive_message' event
#     assert received[0]['name'] == 'receive_message'

#     # Check that the response contains the correct data
#     assert received[0]['args'] == [test_data]

#     # Check that the message was saved to the database
#     message = Message.query.filter_by(content='test_message').first()
#     assert message is not None

if __name__ == "__main__":
    # test_register()
    # test_login()
    # test_get_rooms()
    # test_join_room()
    # test_leave_room()
    test_send_message(app, socketio, db)