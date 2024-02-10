import argparse
from db_utils import create_user, delete_user, get_user, list_tables

def main(): 
    parser = argparse.ArgumentParser(description="CLI for user management")
    parser.add_argument('action', choices=['list', 'create', 'delete', 'get'], help='Action to perform')
    args = parser.parse_args()
    
    if args.action == 'list':
        list_tables()
    elif args.action == 'create':
        name = input("Enter user name to add: ")
        create_user(name)
    elif args.action == 'delete':
        name = input("Enter user name to delete: ")
        delete_user(name)
    elif args.action == 'get':
        name = input("Enter user name to get: ")
        get_user(name)

if __name__ == "__main__":
    main()