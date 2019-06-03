'''

    db.py
    fractal

'''

import sqlite3
import datetime

db_name = "database.db"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def return_user_data(username):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.row_factory = dict_factory

    c.execute("SELECT * FROM fractal_users WHERE username='?'", username)
    conn.commit()

    return c.fetchone()

    conn.close()


def insert_password_token(token, username):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.row_factory = dict_factory

    c.execute("UPDATE fractal_users SET password_token=? WHERE username=?", (token, username))
    conn.commit()

    conn.close()


def return_username_from_email(email):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT username FROM fractal_users WHERE email=?", (email, ))
    conn.commit()

    return c.fetchone()[0]

    conn.close()


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


def return_username_from_user_id(user_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT username FROM fractal_users WHERE id='{user_id}'".format(user_id=user_id)) # this
    conn.commit()

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


def return_user_submissions(id_num):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT * from fractal_activities WHERE user_id='{id}'".format(id=id_num))
    conn.commit()

    return c.fetchall()

    conn.close()


def return_all_user_submissions():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT * from fractal_activities")
    conn.commit()

    return c.fetchall()

    conn.close()


def set_status_of_activity(activity_id, status):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("UPDATE fractal_activities SET approved={status} WHERE submission_id={activity_id}".format(activity_id=activity_id, status=status))
    conn.commit()

    return c.fetchall()

    conn.close()


def insert_new_activity(username, number_of_hours, location, telephone_number, date_completed, counselor):
    date_submitted = datetime.datetime.now().strftime("%Y-%m-%d")

    to_insert = [(return_user_id(username), username, number_of_hours, location, date_submitted, date_completed,
                  telephone_number, counselor)]

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.executemany("INSERT INTO fractal_activities ('user_id', 'name', 'num_of_hours', 'location', 'date_submitted', "
                  "'date_of_completion', 'phone_number', 'counselor') VALUES (?, ?, ?, ?, ?, ?, ?, ?)", to_insert)
    conn.commit()

    conn.close()

