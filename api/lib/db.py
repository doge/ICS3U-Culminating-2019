'''

    db.py
    fractal

'''

import sqlite3

db_name = "database.db"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def return_all_activities():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.row_factory = dict_factory

    c.execute("SELECT * FROM fractal_activities")
    conn.commit()

    return c.fetchall()