from flask import *
from lib.db import *
import hashlib


login_page = Blueprint('login_page', __name__, template_folder='templates')


# The root of our website.
@login_page.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'login_button' in request.form:
            hashed_password = hashlib.sha256(request.form['password'].encode()).hexdigest()
            user_valid = return_valid_user(request.form['username'], hashed_password)
            # If user_valid returns true,
            if user_valid:
                session['user'] = request.form['username']
                return redirect(url_for('home_page.home'))
            else:
                flash('The username or password was incorrect.')
        elif 'register_button' in request.form:
            return redirect(url_for('register_page.register'))

    # If the user is already logged in,
    if g.user:
        return redirect(url_for('home_page.home'))
    else:
        return render_template('login.html')

