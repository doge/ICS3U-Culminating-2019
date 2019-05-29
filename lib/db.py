'''

    db.py
    fractal

'''

import sqlite3
import datetime

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


def return_user_level(username):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT user_level from fractal_users WHERE username='{username}'".format(username=username))
    conn.commit()

    return c.fetchone()[0]

    conn.close()


def return_user_id(username):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT id from fractal_users WHERE username='{username}'".format(username=username))
    conn.commit()

    return c.fetchone()[0]

    conn.close()


def return_counselor_names():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT username from fractal_users WHERE user_level=1")
    conn.commit()

    return c.fetchall()

    conn.close()


def insert_new_activity(username, number_of_hours, location, telephone_number, date_completed, counselor):
    date_submitted = datetime.datetime.now().strftime("%Y-%m-%d")

    to_insert = [(return_user_id(username), username, number_of_hours, location, date_submitted, date_completed,
                  telephone_number, counselor)]

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.executemany("INSERT INTO fractal_activities ('id', 'name', 'num_of_hours', 'location', 'date_submitted', "
                  "'date_of_completion', 'phone_number', 'counselor') VALUES (?, ?, ?, ?, ?, ?, ?, ?)", to_insert)
    conn.commit()

    conn.close()

