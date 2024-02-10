import argparse
from db_utils import create_user, delete_user_name, delete_user_id, get_user, list_tables, print_table_contents

def main(): 
    parser = argparse.ArgumentParser(description="CLI for user management")
    parser.add_argument('action', choices=['list_tables', 'print_table', 'create_user', 'delete_user_name', 'delete_user_id', 'get_user'], help='Action to perform')
    args = parser.parse_args()
    
    if args.action == 'list_tables':
        list_tables()
    elif args.action == 'print_table':
        table_name = input("Enter the table name: ")
        print_table_contents(table_name) 
    elif args.action == 'create_user':
        name = input("Enter user name to add: ")
        create_user(name)
    elif args.action == 'delete_user_name':
        name = input("Enter user name to delete: ")
        delete_user_name(name)
    elif args.action == 'delete_user_id':
        id = input("Enter user id to delete: ")
        delete_user_id(id)
    elif args.action == 'get_user':
        name = input("Enter user name to get: ")
        get_user(name)

if __name__ == "__main__":
    main()