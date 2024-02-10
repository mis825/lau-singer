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
CHECK_IF_USER_NAME_EXISTS = "SELECT id FROM users WHERE name = %s;"
CHECK_IF_USER_ID_EXISTS = "SELECT id FROM users Where id = %s;"
DELETE_USER = "DELETE FROM users WHERE id = %s;"
LIST_TABLES = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"


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
