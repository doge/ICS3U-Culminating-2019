'''

    db.py
    fractal

'''

import sqlite3

db_name = "database.db"


def return_valid_user(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT password FROM fractal_users WHERE username='{username}'".format(username=username))
    conn.commit()

    user_password = [password[0] for password in c.fetchall()]

    if password in user_password:
        return True
    else:
        return False

    conn.close()


def username_exists(username):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT username FROM fractal_users")
    conn.commit()

    existing_username = [username[0] for username in c.fetchall()]

    if username in existing_username:
        return True
    else:
        return False

    conn.close()


def insert_new_user(username, email, password):
    to_insert = [(username, email, password)]

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.executemany("INSERT INTO fractal_users ('username', 'email', 'password') VALUES (?, ?, ?)", to_insert)
    conn.commit()

    conn.close()


def return_user_hours(username):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT total_hours from fractal_users WHERE username='{username}'".format(username=username))
    conn.commit()

    return c.fetchone()[0]

    conn.close()