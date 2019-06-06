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

    c.execute("SELECT * FROM fractal_users WHERE username=?", (username, ))
    conn.commit()

    return c.fetchone()

    conn.close()


def return_user_data_from_id(user_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.row_factory = dict_factory

    c.execute("SELECT * FROM fractal_users WHERE id=?", (user_id, ))
    conn.commit()

    return c.fetchone()

    conn.close()


def return_activity_data(activity_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.row_factory = dict_factory

    c.execute("SELECT * FROM fractal_activities WHERE submission_id=?", (activity_id, ))
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


def return_username_from_name(first_name, last_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT username FROM fractal_users WHERE first_name=? AND last_name=?", (first_name, last_name ))
    conn.commit()

    return c.fetchone()[0]

    conn.close()


def return_valid_user(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("SELECT password FROM fractal_users WHERE username=?", (username, ))
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


def insert_new_user(username, first_name, last_name, email, password):
    to_insert = [(username, first_name, last_name, email, password)]

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.executemany("INSERT INTO fractal_users ('username', 'first_name', 'last_name', 'email', 'password') VALUES (?, ?, ?, ?, ?)", to_insert)
    conn.commit()

    conn.close()


def return_counselor_names():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    #c.row_factory = dict_factory

    c.execute("SELECT first_name, last_name from fractal_users WHERE user_level=1")
    conn.commit()

    return c.fetchall()

    conn.close()


def return_user_submissions(id_num):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.row_factory = dict_factory

    c.execute("SELECT * from fractal_activities WHERE user_id=?", (id_num, ))
    conn.commit()

    return c.fetchall()

    conn.close()


def return_all_user_submissions(counselor):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.row_factory = dict_factory

    c.execute("SELECT * from fractal_activities WHERE counselor=?", (counselor, ))
    conn.commit()

    return c.fetchall()

    conn.close()


def set_status_of_activity(activity_id, status):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute("UPDATE fractal_activities SET approved=? WHERE submission_id=?", (status, activity_id))
    conn.commit()

    return c.fetchall()

    conn.close()


def insert_new_activity(user_id, full_name, number_of_hours, location, telephone_number, date_completed, counselor, student_comment):
    date_submitted = datetime.datetime.now().strftime("%Y-%m-%d")

    to_insert = [(user_id, full_name, number_of_hours, location, date_submitted, date_completed,
                  telephone_number, counselor, student_comment)]

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.executemany("INSERT INTO fractal_activities ('user_id', 'name', 'num_of_hours', 'location', 'date_submitted', "
                  "'date_of_completion', 'phone_number', 'counselor', 'student_comment') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", to_insert)
    conn.commit()

    conn.close()


def update_new_password(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.row_factory = dict_factory

    c.execute("UPDATE fractal_users SET password_token=?, password=? WHERE username=?", (None, password, username))
    conn.commit()

    conn.close()


def update_number_of_hours(user_id, num_of_hours):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.row_factory = dict_factory

    c.execute("UPDATE fractal_users SET total_hours = total_hours + ? WHERE id=?", (num_of_hours, user_id ))
    conn.commit()

    conn.close()