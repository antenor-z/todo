from flask import Flask, render_template, request, redirect, url_for, session, abort
from security import auth
from todo import insert_todo, edit_todo, remove_todo, get_todo, get_todos, switch_todo
from datetime import datetime

app = Flask(__name__)

with open(".secret") as f:
    app.secret_key = f.read().split("\n")[0]

@app.get("/login")
def login_get():
    if session.get("username", None):
        return redirect(url_for('get_all'))
    else:
        return render_template("login.html")

@app.post("/logout")
def logout():
    session.pop("username")
    return redirect(url_for('login_get'))

@app.post("/login")
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    if auth(username, password):
        session["username"] = username
    return redirect(url_for('login_get'))

@app.get("/add")
def add_get():
    user = session.get("username", None)
    if user == None:
        return redirect(url_for('login_get'))
    
    return render_template("add.html")

@app.post("/add")
def add_post():
    user = session.get("username", None)
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

    insert_todo(title=title, desc=desc, created_at=created_at, deadline=deadline, username=user)
    
    return redirect(url_for('get_all'))

@app.get("/")
def get_all():
    user = session.get("username", None)
    if user == None:
        return redirect(url_for('login_get'))
    
    todos = get_todos(user)
    return render_template("get_all.html", todos=todos)

@app.get("/edit/<int:id>")
def edit(id: int):
    user = session.get("username", None)
    if user == None:
        return redirect(url_for('login_get'))
    
    todo = get_todo(user, id)
    return render_template("edit.html", todo=todo)

@app.post("/edit/<int:id>")
def save(id: int):
    user = session.get("username", None)
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

    status = request.form["status"]
   
    edit_todo(title=title, desc=desc, deadline=deadline, status=status, username=user, todo_id=id)
    return redirect(url_for('get_all'))

@app.post("/switch/<int:id>")
def switch(id: int):
    user = session.get("username", None)
    if user == None:
        return redirect(url_for('login_get'))
    
    switch_todo(user, id)
    return redirect(url_for('get_all'))


@app.post("/delete/<int:id>")
def delete_todo(id: int):
    user = session.get("username", None)
    if user == None:
        return redirect(url_for('login_get'))
    
    remove_todo(user, id)
    return redirect(url_for('get_all')) 
