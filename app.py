from flask import Flask, render_template, request, redirect, url_for, session, abort
from security import Auth
from todo import insert_todo, edit_todo, remove_todo, get_todo, get_todos, switch_todo
from datetime import datetime

app = Flask(__name__)

with open(".secret") as f:
    app.secret_key = f.read().split("\n")[0]

auth = Auth(session=session)

@app.get("/login")
def login_get():
    if auth.get_user():
        return redirect(url_for('get_all'))
    else:
        return render_template("login.html")

@app.post("/logout")
def logout():
    session.pop("id")
    return redirect(url_for('login_get'))

@app.post("/login")
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    if auth.auth(username, password):
        auth.make_session(username)
    return redirect(url_for('login_get'))

@app.get("/add")
def add_get():
    user = auth.get_user()
    if user == None:
        return redirect(url_for('login_get'))
    
    return render_template("add.html")

@app.post("/add")
def add_post():
    user = auth.get_user()
    if user == None:
        return redirect(url_for('login_get'))
    
    title = request.form["title"]
    desc = request.form["desc"]
    created_at = datetime.now()
    created_at = created_at.replace(second=0, microsecond=0)

    if title == "": abort(400)

    deadline = request.form["deadline"]
    if deadline != "":
        deadline = datetime.strptime(request.form["deadline"], "%Y-%m-%dT%H:%M")
    else:
        deadline = ""

    priority = request.form["priority"]
    if priority == "None": priority = None
    else:
        try:
            priority = int(priority)
        except ValueError:
            abort(400)
        if priority not in [0, 1, 2]: abort(400)

    insert_todo(title=title, desc=desc, created_at=created_at, deadline=deadline, priority=priority, username=user)
    
    return redirect(url_for('get_all'))

@app.get("/")
def get_all():
    user = auth.get_user()
    if user == None:
        return redirect(url_for('login_get'))
    
    todos = get_todos(user)

    for todo in todos:
        if len(todo["desc"].split("\n")) > 4:
            todo["needsShowMore"] = True
        else:
            todo["needsShowMore"] = False

    return render_template("get_all.html", todos=todos)

@app.get("/edit/<int:id>")
def edit(id: int):
    user = auth.get_user()
    if user == None:
        return redirect(url_for('login_get'))
    
    todo = get_todo(user, id)
    return render_template("edit.html", todo=todo)

@app.post("/edit/<int:id>")
def save(id: int):
    user = auth.get_user()
    if user == None:
        return redirect(url_for('login_get'))
    
    title = request.form["title"]
    desc = request.form["desc"]

    if title == "": abort(400)

    deadline = request.form["deadline"]
    if deadline != "":
        deadline = datetime.strptime(request.form["deadline"], "%Y-%m-%dT%H:%M")
    else:
        deadline = ""

    priority = request.form["priority"]
    if priority == "None": priority = None
    else:
        try:
            priority = int(priority)
        except ValueError:
            abort(400)
        if priority not in [0, 1, 2]: abort(400)

    status = request.form["status"]
   
    edit_todo(title=title, desc=desc, deadline=deadline, status=status, priority=priority, username=user, todo_id=id)
    return redirect(url_for('get_all'))

@app.post("/switch/<int:id>")
def switch(id: int):
    user = auth.get_user()
    if user == None:
        return redirect(url_for('login_get'))
    
    switch_todo(user, id)
    return redirect(url_for('get_all'))


@app.post("/delete/<int:id>")
def delete_todo(id: int):
    user = auth.get_user()
    if user == None:
        return redirect(url_for('login_get'))
    
    remove_todo(user, id)
    return redirect(url_for('get_all')) 

