from flask import *
from lib.db import *
from lib.mailer import *
from lib.misc import *
import hashlib

prereset_page = Blueprint('prereset_page', __name__, template_folder='templates')


@prereset_page.route('/reset',methods=['GET', 'POST'])
def pre_reset():
    if request.method == "POST":
        try:
            token = generate_token(32)
            username = return_username_from_email(request.form['email'])
            # insert our token into the database
            insert_password_token(token, username)
            # send the user the link to reset their password
            send_mail(request.form['email'], 'The link to reset your password is example.com/%s/%s' % (username, token))
            flash('A link to reset your password has been sent to your email address.', 'success')
        except:
            flash('No user with that email exists.', 'danger')

    return render_template('reset_auth.html')


reset_page = Blueprint('reset_page', __name__, template_folder='templates')


@reset_page.route('/reset/<username>/<token>', methods=['GET', 'POST'])
def reset(username, token):
    if request.method == "POST":
        if not username_exists(request.form['username']):
            flash('No user with that username exists.', 'danger')
        else:
            if request.form['token'] == return_user_data(request.form['username'])['password_token']:
                hashed_password = hashlib.sha256(request.form['password'].encode()).hexdigest()
                update_new_password(request.form['username'], hashed_password)
                flash(Markup('Your password has been updated! <a href="/login">Click here to login.</a>'), 'success')
            else:
                flash('Your password reset token was incorrect.', 'danger')

    return render_template('reset.html', username=username, token=token)
