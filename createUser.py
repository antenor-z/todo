from db import db_exec
from security import hash_password

def create_user(username, password):
    (password_salt, password_hash) = hash_password(password)
    db_exec(f"""INSERT INTO user (username, pass_salt, pass_hash) 
            VALUES ('{username}', '{password_salt}', '{password_hash}');""")
    
if __name__ == "__main__":
    username = input("Name: ")
    password = input("Password: ")
    create_user(username, password)
