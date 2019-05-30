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

            * students *
                [x] submit a request form
                [x] display all requests on home

            * counselors *
                [x] approval of requests

        * verification process *
            [ ] setup auto-mailer -> google smtp server
            [x] different user accounts (administrator -> counselor -> student)

        * finishing touches *
            [x] table on /home that displays all requests

        * organization *
            [ ] put routes into separate files -> create a directory (/routes) [use 'blueprints']


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

        g.counselor_list = []  # our list of counselors
        for name in return_counselor_names():
            g.counselor_list.append(name)
        g.counselor_list = [x[0] for x in g.counselor_list]


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if g.user and g.level == "student":
        if request.method == "POST":
            if "submit_button" in request.form:
                insert_new_activity(g.user, request.form['number_of_hours'], request.form['location'], request.form['number_of_location'], request.form['date_of_completion'], request.form['counselor'])
                flash('Your submission was successful!', 'success')

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
        return redirect(url_for('home'))
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
                flash('One of the fields was not filled in.', 'danger')
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
        if request.method == "POST":
            if "approve_button" in request.form:
                set_status_of_activity(request.form['approve_button'], 1)
            elif "deny_button" in request.form:
                set_status_of_activity(request.form['deny_button'], 2)

        if g.level == "student":
            submissions = return_user_submissions(return_user_id(g.user))
            return render_template('home.html', submissions=submissions)
        elif g.level == "counselor":
            submissions = return_all_user_submissions()
            print(submissions)
            return render_template('home.html', submissions=submissions)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
