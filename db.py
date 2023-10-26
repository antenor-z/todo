import sqlite3

def db_exec(command, params):
    conn = sqlite3.connect('database.sqlite3')
    cursor = conn.cursor()

    res = None

    try:
        cursor.execute(command, params)
        res = cursor.fetchall()
    except Exception as e:
        conn.rollback()
        print("NOT EXECUTED due to error:")
        print(e)
    else:
        conn.commit()

    conn.close()

    return res
