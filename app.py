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
            [x] setup auto-mailer -> google smtp server
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

from api.submissions import api_submissions

import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

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

app.register_blueprint(api_submissions)


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        # 'g' is a namespace object that has the same lifetime as an application context.
        g.user = session['user']
        g.level = list(user_levels.keys())[list(user_levels.values()).index(return_user_data(session['user'])['user_level'])]


@app.route('/')
def root():
    ''' When anyone loads the root of the website, it redirects them to the login screen. '''
    return redirect(url_for('login_page.login'))


@app.route('/logout')
def logout():
    ''' Allows a user in a session to logout. '''
    session.pop('user', None)
    return redirect(url_for('login_page.login'))


if __name__ == '__main__':
    app.run()
