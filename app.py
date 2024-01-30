from flask import Flask

app = Flask(__name__)

@app.get("/")
def home(): 
    return "Home Page"

@app.get("/create-user")
def create_user(): 
    return "Please enter a username"



