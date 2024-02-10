import os
import random
import logging
import psycopg2
from dotenv import load_dotenv

# Load environment variables and database connection URL
load_dotenv()
url = os.getenv("DATABASE_URL")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# SQL Queries
CREATE_USERS_TABLE = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT);"
INSERT_USER_RETURN_ID = "INSERT INTO users (name) VALUES (%s) RETURNING id;"
CHECK_IF_USER_NAME_EXISTS = "SELECT id FROM users WHERE name = %s;"
CHECK_IF_USER_ID_EXISTS = "SELECT id FROM users Where id = %s;"
DELETE_USER = "DELETE FROM users WHERE id = %s;"
LIST_TABLES = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"

# SQL Room Related Queries
CREATE_ROOMS_TABLE = """
CREATE TABLE IF NOT EXISTS rooms (
    id VARCHAR(6) PRIMARY KEY,
    name TEXT NOT NULL,
    max_users INT,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
);
"""

CREATE_ROOM_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS room_users (
    room_id VARCHAR(6) REFERENCES rooms(id),
    user_id INT REFERENCES users(id),
    joined_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    PRIMARY KEY (room_id, user_id)
);
"""

CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    room_id VARCHAR(6) REFERENCES rooms(id),
    user_id INT REFERENCES users(id),
    message_text TEXT NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
);
"""


def initialize_db():
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_ROOMS_TABLE)
            cursor.execute(CREATE_ROOM_USERS_TABLE)
            cursor.execute(CREATE_MESSAGES_TABLE)
    logger.info("Database initialized with user and room functionality.")


def create_user(name):
    """Create a new user with the given name."""
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CHECK_IF_USER_NAME_EXISTS, (name,))
            existing_user_id = cursor.fetchone()
            if existing_user_id:
                logger.warning(f"User: '{name}' already exists")
                return {"message": f"User: '{name}' already exists"}, 400
            cursor.execute(INSERT_USER_RETURN_ID, (name,))
            user_id = cursor.fetchone()[0]
            logger.info(f"User '{name}' created with ID: {user_id}.")
            return {"id": user_id, "message": f"User: '{name}' created"}, 201


def delete_user_name(name):
    """Delete a user by name."""
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(CHECK_IF_USER_NAME_EXISTS, (name,))
            user_id = cursor.fetchone()
            if user_id:
                cursor.execute(DELETE_USER, (user_id,))
                logger.info(f"User '{name}' deleted.")
                return {"message": f"User '{name}' deleted"}, 200
            else:
                logger.warning(f"User '{name}' not found")
                return {"message": "User not found"}, 404


def delete_user_id(id):
    """Delete a user by name."""
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(CHECK_IF_USER_ID_EXISTS, (id,))
            user_id = cursor.fetchone()
            if user_id:
                cursor.execute(DELETE_USER, (user_id,))
                logger.info(f"User with id: '{id}' deleted.")
                return {"message": f"User with id: '{id}' deleted"}, 200
            else:
                logger.warning(f"User with id: '{id}' not found")
                return {"message": "User not found"}, 404


def get_user(name):
    """Retrieve a user by name."""
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(CHECK_IF_USER_NAME_EXISTS, (name,))
            user_id = cursor.fetchone()
            if user_id:
                logger.info(f"User '{name}' found with ID: {user_id[0]}.")
                return {"id": user_id[0], "message": f"User '{name}' found"}, 200
            else:
                logger.warning(f"User '{name}' not found")
                return {"message": "User not found"}, 404


def list_tables():
    """List all tables in the public schema of the database."""
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(LIST_TABLES)
            tables = cursor.fetchall()
            if tables:
                table_names = [table[0] for table in tables]
                logger.info(f"Tables found: {table_names}")
                return {"tables": table_names, "message": "Tables listed"}, 200
            else:
                logger.info("No tables found in the database.")
                return {"message": "No tables found"}, 404


def print_table_contents(table_name):
    """Prints the contents of a specified table."""
    query = f"SELECT * FROM {table_name};"
    
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                if rows:
                    # Fetch column names from cursor.description
                    colnames = [desc[0] for desc in cursor.description]
                    print(f"Contents of table '{table_name}':")
                    print(", ".join(colnames))  # Print column names
                    for row in rows:
                        print(row)
                    logger.info(f"Printed contents of table '{table_name}'.")
                    return {"message": f"Printed contents of table '{table_name}'", "code": 200}
                else:
                    logger.info(f"Table '{table_name}' is empty or does not exist.")
                    return {"message": "Table is empty or does not exist", "code": 404}
            except psycopg2.Error as e:
                logger.error(f"Error accessing table '{table_name}': {e}")
                return {"message": f"Error accessing table '{table_name}': {e}", "code": 500}


def generate_unique_room_id():
    """Generates a unique 6-digit room ID."""
    while True:
        room_id = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        if not room_id_exists(room_id):
            return room_id


def room_id_exists(room_id):
    """Check if a room exists based on the given id."""
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM rooms WHERE id = %s;", (room_id,))
            # return true if the room exists, false otherwise 
            return cursor.fetchone() is not None
        
        
def create_room(name, max_users):
    """Creates a new room with the given name and maximum user limit."""
    room_id = generate_unique_room_id() 
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO rooms (id, name, max_users) VALUES (%s, %s, %s);", (room_id, name, max_users))
            conn.commit()  # Ensure data consistency and durability
    logger.info(f"Room '{name}' created with ID: {room_id}.")
    return {"id": room_id, "name": name, "max_users": max_users}, 201


def join_room(user_id, room_id):
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            # check if the room exists
            cursor.execute("SELECT max_users FROM rooms WHERE id = %s;", (room_id,))
            room = cursor.fetchone()
            if not room:
                return {"message": "Room does not exist"}, 404
            
            # check if the room is full
            cursor.execute("SELECT COUNT(user_id) FROM room_users WHERE room_id = %s;", (room_id,))
            user_count = cursor.fetchone()[0]
            if user_count >= room[0]: 
                return {"message": "Room is full"}, 400
            
            # if everything is good
            cursor.execute("INSERT INTO room_users (room_id, user_id) VALUES (%s, %s);", (room_id, user_id))
            conn.commit()
            return {"message": f"User with id: {user_id} added to room: {room_id} successfully"}, 200

