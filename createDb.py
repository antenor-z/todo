from db import db_exec

db_exec('''
CREATE TABLE IF NOT EXISTS user (
    username TEXT PRIMARY KEY NOT NULL,
    pass_salt TEXT NOT NULL,
    pass_hash TEXT NOT NULL
);
''', ())

db_exec('''
CREATE TABLE IF NOT EXISTS todo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    desc TEXT,
    created_at DATETIME NOT NULL,
    deadline DATETIME,
    status TEXT NOT NULL,
    priority INTEGER,
    username TEXT NOT NULL,
    FOREIGN KEY (username) REFERENCES user(username)
);
''', ())
