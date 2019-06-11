from flask import *
from lib.db import *

home_page = Blueprint('home_page', __name__, template_folder='templates')


@home_page.route('/home', methods=['GET', 'POST'])
def home():
    '''
        Gathers all 'requests' as well as the users first name, and the total number of hours they have, and displays
        this information to the user.
    '''
    if g.user:
        if request.method == "POST":
            if "approve_button" in request.form:
                set_status_of_activity(request.form['approve_button'], 1)
                update_number_of_hours(return_activity_data(request.form['approve_button'])['user_id'],
                                       return_activity_data(request.form['approve_button'])['num_of_hours'])
            elif "deny_button" in request.form:
                set_status_of_activity(request.form['deny_button'], 2)

        first_name = return_user_data(g.user)['first_name']
        total_hours = return_user_data(session['user'])['total_hours']

        if g.level == "student":
            submissions = return_user_submissions(return_user_data(g.user)['id'])
        elif g.level == "counselor":
            counselor_name = "%s %s" % (return_user_data(g.user)['first_name'], return_user_data(g.user)['last_name'])
            submissions = return_all_user_submissions(counselor_name)

        return render_template('home.html', submissions=submissions, first_name=first_name, total_hours=total_hours)
    else:
        return redirect(url_for('login_page.login'))

