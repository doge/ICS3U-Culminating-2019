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
            [x] put blueprints into separate files -> create a directory (/blueprints) [use 'blueprints']


'''

from flask import *
from lib.db import *

from blueprints.grant import grant_page
from blueprints.login import login_page
from blueprints.register import register_page

from blueprints.reset import reset_page
from blueprints.reset import prereset_page

from blueprints.home import home_page
from blueprints.submit import submit_page

import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

user_levels = {
    'student': 0,
    'counselor': 1,
    'admin': 2
}

app.register_blueprint(grant_page)
app.register_blueprint(home_page)
app.register_blueprint(login_page)
app.register_blueprint(register_page)
app.register_blueprint(reset_page)
app.register_blueprint(prereset_page)
app.register_blueprint(submit_page)


# This is called before a request is made to the server.
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        # 'g' is a namespace object that has the same lifetime as an application context.
        g.user = session['user']
        g.total_hours = return_user_data(session['user'])['total_hours']
        g.level = list(user_levels.keys())[list(user_levels.values()).index(return_user_data(session['user'])['user_level'])]

        g.counselor_list = []  # our list of counselors
        for name in return_counselor_names():
            g.counselor_list.append("%s %s" % (name[0], name[1]))


@app.route('/')
def root():
    return redirect(url_for('login_page.login'))


# The logout page of our website.
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login_page.login'))


if __name__ == '__main__':
    app.run()
