import hashlib
import os
import base64

from db import db_exec

class Auth:
    # dict from session_id (random) to username
    active_sessions = {}

    # Flask's session
    session = ""

    def __init__(self, session):
        self.session = session

    def hash_password(self, password: str) -> dict:
        salt = os.urandom(16)
        sha256 = hashlib.sha256()
        sha256.update(salt)
        sha256.update(password.encode('utf-8'))

        hash_value = sha256.hexdigest()

        return (salt.hex(), hash_value)

    def check_password(self, salt: str, correct_hash: str, provided_password: str) -> bool:
        sha256 = hashlib.sha256()
        sha256.update(bytes.fromhex(salt))
        sha256.update(provided_password.encode('utf-8'))

        hash_value = sha256.hexdigest()

        return hash_value == correct_hash

    def auth(self, username, password) -> bool:
        res = db_exec("SELECT pass_salt, pass_hash from USER WHERE username=?", (username, ))
        
        if len(res) != 1:
            return False
        
        (pass_salt, pass_hash) = res[0]
        
        return self.check_password(pass_salt, pass_hash, password)

    def make_session(self, username):
        session_id = base64.b64encode(os.urandom(16)).decode('utf-8')
        self.active_sessions[session_id] = username
        self.session["id"] = session_id

    def get_user(self):
        session_id = self.session.get("id")
        if session_id == None: return None
        return self.active_sessions.get(session_id, None)

if __name__ == "__main__":
    aa = Auth(None)
    (salt, hashh) = aa.hash_password('DEADBEEF')
    assert aa.check_password(salt, hashh, "DEADBEEF") == True 
    assert aa.check_password(salt, hashh, "DEEDBEEF") == False 
    print("test OK")