import hashlib
import os

from db import db_exec

def hash_password(password: str) -> dict:
    salt = os.urandom(16)
    sha256 = hashlib.sha256()
    sha256.update(salt)
    sha256.update(password.encode('utf-8'))

    hash_value = sha256.hexdigest()

    return (salt.hex(), hash_value)

def check_password(salt: str, correct_hash: str, provided_password: str) -> bool:
    sha256 = hashlib.sha256()
    sha256.update(bytes.fromhex(salt))
    sha256.update(provided_password.encode('utf-8'))

    hash_value = sha256.hexdigest()

    return hash_value == correct_hash

def auth(username, password) -> bool:
    res = db_exec(f"SELECT pass_salt, pass_hash from USER WHERE username='{username}'")
    
    if len(res) != 1:
        return False
    
    (pass_salt, pass_hash) = res[0]
    
    return check_password(pass_salt, pass_hash, password)

if __name__ == "__main__":
    (salt, hashh) = hash_password('DEADBEEF')
    assert check_password(salt, hashh, "DEADBEEF") == True 
    assert check_password(salt, hashh, "DEEDBEEF") == False 
    print("test OK")

    
