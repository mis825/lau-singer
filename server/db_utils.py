import os
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
CHECK_IF_USER_EXISTS = "SELECT id FROM users WHERE name = %s;"
DELETE_USER = "DELETE FROM users WHERE id = %s;"
LIST_TABLES_QUERY = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"

def create_user(name):
    """Create a new user with the given name."""
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CHECK_IF_USER_EXISTS, (name,))
            existing_user_id = cursor.fetchone()
            if existing_user_id:
                logger.warning(f"User: '{name}' already exists")
                return {"message": f"User: '{name}' already exists"}, 400
            cursor.execute(INSERT_USER_RETURN_ID, (name,))
            user_id = cursor.fetchone()[0]
            logger.info(f"User '{name}' created with ID: {user_id}.")
            return {"id": user_id, "message": f"User: '{name}' created"}, 201

def delete_user(name):
    """Delete a user by name."""
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(CHECK_IF_USER_EXISTS, (name,))
            user_id = cursor.fetchone()
            if user_id:
                cursor.execute(DELETE_USER, (user_id,))
                return f"User '{name}' deleted."
            else:
                return "User not found."

def get_user(name):
    """Retrieve a user by name."""
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(CHECK_IF_USER_EXISTS, (name,))
            result = cursor.fetchone()
            if result:
                return f"User '{name}' found with ID: {result[0]}."
            else:
                return "User not found."

def list_tables():
    """List all tables in the public schema of the database."""
    with psycopg2.connect(url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(LIST_TABLES_QUERY)
            tables = cursor.fetchall()
            if tables:
                return [table[0] for table in tables]
            else:
                return "No tables found."

