from flask import *
from lib.db import *
import hashlib

register_page = Blueprint('register_page', __name__, template_folder='templates')


# The registration page of our website.
@register_page.route('/register', methods=['GET', 'POST'])
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
                    insert_new_user(request.form['username'], request.form['first_name'], request.form['last_name'], request.form['email'], hashed_password)
                    flash('Your registration was successful!', 'success')
            else:
                flash('One of the fields was not filled in.', 'danger')
        elif 'login_button' in request.form:
            return redirect(url_for('login_page.login'))

    return render_template('register.html')

