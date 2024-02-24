from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from app import app, db, User  

load_dotenv()

def create_user(username, password):
    # hasing the password for security
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # create a new user
    new_user = User(username=username, password_hash=hashed_password)
    
    # have to use app.app_context() to access the database
    with app.app_context():
        # add the new user to the session
        db.session.add(new_user)
        try:
            # commit the session to the database
            db.session.commit()
            print(f"User '{username}' created successfully.")
        except Exception as e:
            # rollback the session if there is an error
            db.session.rollback()
            print(f"Failed to create user '{username}'. Error: {e}")

if __name__ == '__main__':
    # create a test user here 
    username = ''
    password = ''
    create_user(username, password)
