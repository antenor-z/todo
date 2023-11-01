from createUser import create_user
from security import auth
from db import db_exec
from todo import insert_todo, get_todos, get_todo, remove_todo, switch_todo

create_user("fakeuser", "badpassword")
ret = db_exec("SELECT * FROM user WHERE username = 'fakeuser'", ())
assert len(ret) == 1
assert auth("fakeuser", "badpassword") == True
assert auth("fakeuser", "123") == False

insert_todo("t", "d", "2023-01-01", "2023-01-05", 1, "fakeuser")
todos = get_todos("fakeuser")
assert len(todos) == 1
assert todos[0]["title"] == "t"
assert todos[0]["desc"] == "d"
assert todos[0]["created_at"] == "2023-01-01"
assert todos[0]["deadline"] == "2023-01-05"
assert todos[0]["status"] == "TODO"
assert todos[0]["priority"] == 1

todo = get_todo("fakeuser", todos[0]["id"])
assert todo["title"] == "t"
assert todo["desc"] == "d"
assert todo["created_at"] == "2023-01-01"
assert todo["deadline"] == "2023-01-05"
assert todo["status"] == "TODO"
assert todos["priority"] == 1

insert_todo("a", "b", "2023-02-01", "2023-02-05", 0, "fakeuser")
todos = get_todos("fakeuser")
assert len(todos) == 2
assert todos[0]["title"] == "t"
assert todos[0]["desc"] == "d"
assert todos[0]["created_at"] == "2023-01-01"
assert todos[0]["deadline"] == "2023-01-05"
assert todos[0]["status"] == "TODO"
assert todos[0]["priority"] == 1
assert todos[1]["title"] == "a"
assert todos[1]["desc"] == "b"
assert todos[1]["created_at"] == "2023-02-01"
assert todos[1]["deadline"] == "2023-02-05"
assert todos[1]["status"] == "TODO"
assert todos[1]["priority"] == 0

todo2 = get_todo("fakeuser", todos[1]["id"])
assert todo2["title"] == "a"
assert todo2["desc"] == "b"
assert todo2["created_at"] == "2023-02-01"
assert todo2["deadline"] == "2023-02-05"
assert todo2["status"] == "TODO"
assert todo2["priority"] == 1

switch_todo("fakeuser", todo["id"])
todo = get_todo("fakeuser", todo["id"])
assert todo["status"] == "DOING"
switch_todo("fakeuser", todo["id"])
todo = get_todo("fakeuser", todo["id"])
assert todo["status"] == "DONE"
switch_todo("fakeuser", todo["id"])
todo = get_todo("fakeuser", todo["id"])
assert todo["status"] == "DONE"

todo2 = get_todo("fakeuser", todo2["id"])
assert todo2["status"] == "TODO"

remove_todo("fakeuser", todo["id"])
remove_todo("fakeuser", todo2["id"])


assert len(get_todos("fakeuser")) == 0

db_exec("DELETE FROM user WHERE username = 'fakeuser'")
ret = db_exec("SELECT * FROM user WHERE username = 'fakeuser'")
assert len(ret) == 0

print("Test OK")
