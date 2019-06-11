from flask import *
from lib.db import *

grant_page = Blueprint('grant_page', __name__, template_folder='templates')


@grant_page.route('/grant', defaults={'token': None}, methods=['GET', 'POST'])
@grant_page.route('/grant/<token>', methods=['GET', 'POST'])
def grant(token):
    '''
        Allows anyone with a valid post token to add a granters comment to the post that contains the post token.
        (These can only be used once)
    '''
    if request.method == "POST":
        try:
            if request.form['token'] == return_activity_data_from_token(request.form['token'])['post_token']:
                update_granter_comment(request.form['comment'], request.form['token'])
                flash('Your comment has been added successfully.', 'success')
        except:
            flash('Your token is invalid.', 'danger')

    return render_template('grant.html', token=token)

