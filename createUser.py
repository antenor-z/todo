from db import db_exec
from security import Auth
from getpass import getpass

def create_user(username, password):
    auth = Auth(None)
    (password_salt, password_hash) = auth.hash_password(password)
    db_exec(f"""INSERT INTO user (username, pass_salt, pass_hash) 
            VALUES ('{username}', '{password_salt}', '{password_hash}');""", ())
    
if __name__ == "__main__":
    try:
        username = input("Name: ")
        while True:
            password = getpass("Password: ")
            password2 = getpass("Repeat password: ")
            if password == password2: break
            print("The two passwords are not equal.")
        
        create_user(username, password)
    except:
        print("\nCtrl+C was pressed, going away. No user created.")

    
