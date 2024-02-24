import os
from dotenv import load_dotenv
from app import app, db, Room, generate_room_code  # Replace 'your_flask_app' with the actual name of your Flask app module

# Load environment variables
load_dotenv()

def create_room():
    with app.app_context():
        # Create the room code
        room_code = generate_room_code()
        
        # Create a new room instance
        new_room = Room(code=room_code)
        
        # Add the new room to the database
        db.session.add(new_room)
        try:
            # Commit the session to the database
            db.session.commit()
            print(f"Room with code '{room_code}' created successfully.")
            return room_code
        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            print(f"Failed to create room. Error: {e}")
            return None

if __name__ == '__main__':
    # Example usage
    create_room()
