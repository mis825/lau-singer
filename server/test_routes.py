import requests

# Test the /register route
def test_register():
    response = requests.post('http://localhost:5000/register', data={
        'username': 'testuser'
    })
    print(response.json())

# Test the /login route
def test_login():
    response = requests.post('http://localhost:5000/login', data={
        'username': 'testuser'
    })
    print(response.json())

if __name__ == "__main__":
    test_register()
    test_login()