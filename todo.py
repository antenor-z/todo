import sqlite3
from security import hash_password
from db import db_exec
from util import human_deadline

def insert_todo(title, desc, created_at, deadline, username):
    db_exec("""INSERT INTO todo (title, desc, created_at, deadline, status, username) VALUES
                (?, ?, ?, ?, 'TODO', ?);
            """, (title, desc, created_at, deadline, username))

def remove_todo(username, todo_id):
    db_exec("DELETE FROM todo WHERE id = ? AND username = ?", (todo_id, username))

def edit_todo(title, desc, deadline, status, username, todo_id):
    if status not in ["TODO", "DOING", "DONE"]:
        raise Exception("status needs to be TODO, DOING or DONE")

    db_exec("""UPDATE todo SET title = ?,
                                desc = ?,
                                deadline = ?,
                                status = ?
            WHERE username = ? AND id = ?""",
            (title, desc, deadline, status, username, todo_id))

def get_todos(username):
    res = db_exec("""SELECT id, title, desc, created_at, deadline, status FROM todo 
                  WHERE username = ? ORDER BY deadline""", (username, ))
    
    todos = []
    for r in res:
        todos.append({"id": r[0], "title": r[1], "desc": r[2], 
                      "created_at": r[3], "deadline": human_deadline(r[4]), "status": r[5]})
            
    return todos

def get_todo(username, todo_id):
    res = db_exec("""SELECT id, title, desc, created_at, deadline, status FROM todo 
                  WHERE id = ? AND username = ?""", (todo_id, username))
    
    if len(res) == 0: return None

    res = res[0]

    return {"id": res[0], "title": res[1], "desc": res[2], 
            "created_at": res[3], "deadline": res[4], "status": res[5]}

def switch_todo(username, todo_id):
    todo = get_todo(username, todo_id)
    status = todo["status"]
    todo_id = todo["id"]
    new_status = status

    if status == "TODO":
        new_status = "DOING"
    elif status == "DOING":
        new_status = "DONE"

    if status != new_status:
        db_exec("UPDATE todo SET status = ? WHERE username = ? AND id = ?",
                (new_status, username, todo_id))
    
