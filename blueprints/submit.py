from flask import *
from lib.db import *
from lib.misc import *

submit_page = Blueprint('submit_page', __name__, template_folder='templates')


@submit_page.route('/submit', methods=['GET', 'POST'])
def submit():
    if g.user and g.level == "student":
        if request.method == "POST":
            if "submit_button" in request.form:
                user_data = return_user_data(g.user)
                name_list = request.form['counselor'].split(" ")
                token = generate_token(32)
                insert_new_activity(user_data['id'], "%s %s" % (user_data['first_name'], user_data['last_name']),
                                    request.form['number_of_hours'], request.form['location'],
                                    request.form['number_of_location'], request.form['date_of_completion'],
                                    "%s %s" % (name_list[0], name_list[1]),
                                    request.form['comment'], token, request.form['granter_email'])
                flash('Your submission was successful!', 'success')

        return render_template("submit.html")
    else:
        return redirect(url_for('home_page.home'))

