import os 
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request

CREATE_USERS_TABLE = (
    "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT);"
)

# value for name is currently a placeholder, have to provide value during execution
INSERT_USER_RETURN_ID = (
    "INSERT INTO users (name) VALUES (%s) RETURNING id;"
)

# searches the user table and return an id for the row (if exists) where the name is matched
CHECK_IF_USER_EXISTS = (
    "SELECT id FROM users WHERE name = %s;"
)

# delete the user if it exists via its row id
DELETE_USER = (
    "DELETE FROM users WHERE id = %s;"
)

# read in environment variables in .env 
load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
# connect to the postgres db 
connection = psycopg2.connect(url)

@app.get("/")
def home(): 
    return "Home Page"

@app.post("/api/create-user")
def create_user(): 
    # for now data input is in json via postman, get_json makes the data a dictionary to easier parsing
    data = request.get_json() 
    user_name = data["name"]
    
    with connection: 
        # a cursor allows us to insert or retrieve data from the db
        with connection.cursor() as cursor:
            # creates the room only once because we specified it in the query
            cursor.execute(CREATE_USERS_TABLE)
            
            # checks if the username already exists
            cursor.execute(CHECK_IF_USER_EXISTS, (user_name,))
            # fetchone() fetches the result of the previous function, only returns id or None
            existing_user_id = cursor.fetchone()
            if existing_user_id: 
                return {"message": f"User: '{user_name}' already exists"}, 400
            
            # if username doesn't exist, add the new user
            cursor.execute(INSERT_USER_RETURN_ID, (user_name,))
            # retrieve the id, fetchone() returns only one row, but this works because we only added one row
            # [0] to avoid tuple 
            user_id = cursor.fetchone()[0]
            
    return {"id": user_id, "message": f"User: '{user_name}' created"}, 201

@app.delete("/api/delete-user")
def delete_user():
    data = request.get_json()
    user_name = data["name"]
    
    with connection: 
        with connection.cursor() as cursor: 
            # check if the user exists
            cursor.execute(CHECK_IF_USER_EXISTS, (user_name,))
            existing_user_id = cursor.fetchone()
            
            if not existing_user_id:
                return {"message": f"User: '{user_name} not found"}, 404
            
            user_id = existing_user_id[0]
            cursor.execute(DELETE_USER, (user_id,))
    
    return {"message": f"User: '{user_name} deleted successfully"}, 200
            