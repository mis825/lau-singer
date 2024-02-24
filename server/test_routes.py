import requests

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
    response = requests.get('http://localhost:5000/join/367757')
    print(response.status_code)

if __name__ == "__main__":
    test_register()
    test_login()
    test_get_rooms()
    test_join_room()