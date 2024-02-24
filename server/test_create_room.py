import os
from dotenv import load_dotenv
from app import app, db, Room, generate_room_code 

load_dotenv()

def create_room():
    with app.app_context():
        # create a new room
        room_code = generate_room_code()
        
        # create a new room instance
        new_room = Room(code=room_code)
        
        # add the new room to the database
        db.session.add(new_room)
        try:
            # commit the session to the database
            db.session.commit()
            print(f"Room with code '{room_code}' created successfully.")
            return room_code
        except Exception as e:
            # rollback the session if there is an error
            db.session.rollback()
            print(f"Failed to create room. Error: {e}")
            return None

if __name__ == '__main__':
    create_room()
