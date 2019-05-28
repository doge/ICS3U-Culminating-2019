'''

    app.py
    fractal

    [x] = done
    [~] = in progress
    [ ] = to do

    * user levels *
        0 -> student
        1 -> counselor
        2 -> administrator

    * things to do *

        * basic functionality*
            [x] login/registration system -> sqlite3 db
            [x] sessions

        * verification process *
            [ ] setup auto-mailer -> google smtp server
            [~] different user accounts (administrator -> counselor -> student)


'''

from flask import *
from lib.db import *
import os
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)

user_levels = {
    'student': 0,
    'counselor': 1,
    'admin': 2
}


# This is called before a request is made to the server.
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        # 'g' is a namespace object that has the same lifetime as an application context.
        g.user = session['user']
        g.total_hours = return_user_hours(session['user'])
        g.level = list(user_levels.keys())[list(user_levels.values()).index(return_user_level(session['user']))]
        g.data = ['test 1', 'test 2', 'test 3']  # this will be our array of counselors, make a function that grabs them
        # and returns them all with a list


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/submit')
def submit():
    print(g.level)
    if g.user and g.level == "student":
        return render_template("submit.html")
    else:
        return redirect(url_for('home'))


# The root of our website.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'login_button' in request.form:
            hashed_password = hashlib.sha256(request.form['password'].encode()).hexdigest()
            user_valid = return_valid_user(request.form['username'], hashed_password)
            # If user_valid returns true,
            if user_valid:
                session['user'] = request.form['username']
                return redirect(url_for('home'))
            else:
                flash('The username or password was incorrect.')
        elif 'register_button' in request.form:
            return redirect(url_for('register'))

    # If the user is already logged in,
    if g.user:
        return redirect(url_for('solve'))
    else:
        return render_template('login.html')


# The registration page of our website.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if 'register_button' in request.form:
            # Check if all the required fields are filled out,
            if len(request.form['username']) > 0 and len(request.form['email']) > 0 and len(request.form['password']) > 0:
                existing_user = username_exists(request.form['username'])
                # If a user already exists with that username,
                if existing_user:
                    flash('A person with the username \"%s\" already exists.' % request.form['username'], 'danger')
                else:
                    hashed_password = hashlib.sha256(request.form['password'].encode()).hexdigest()
                    insert_new_user(request.form['username'], request.form['email'], hashed_password)
                    flash('Your registration was successful!', 'success')
            else:
                flash('One of the fields was not filled in.')
        elif 'login_button' in request.form:
                return redirect(url_for('login'))

    return render_template('register.html')


# The logout page of our website.
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# The homepage of our website.
@app.route('/home', methods=['GET', 'POST'])
def home():
    if g.user:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
