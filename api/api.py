'''
    Allows any counselor/developer with a valid API token to access the API.
'''

from flask import *
from lib.db import *
from api.lib.db import *
from lib.misc import *

api = Blueprint('api', __name__, template_folder='templates')


@api.route('/api', methods=['GET','POST'])
def api_root():
    if g.user and g.level == "counselor":
        if request.method == 'POST':
            if 'generate_button' in request.form:
                try:
                    update_api_token(generate_token(32), g.user)
                    flash('Your API token has been successfully updated.', 'success')
                except Exception as e:
                    flash('An error has occurred. %s' % e)

        api_token = return_user_data(g.user)['api_token']
        submission_url = request.base_url + '/submissions'
        return render_template('developer.html', api_token=api_token, submission_url=submission_url)
    else:
        flash('You are not logged in.', 'danger')
        return redirect(url_for('root'))


@api.route('/api/submissions', methods=['GET'])
def api_gather_submissions():
    '''
        Displays all submission data in JSON format. You can select them all or you can select a specific one with the
        'id' variable.
    '''
    if request.args.get('api_token') in return_api_tokens():
        if request.args.get('id'):
            try:
                data = return_all_activities()[int(request.args.get('id'))]
                resp = jsonify(data)

                return resp
            except Exception as e:
                return jsonify({'error_message': str(e)})
        else:
            data = return_all_activities()
            resp = jsonify(data)

            return resp
    else:
        return jsonify({'error_message': 'Your token is invalid.'})

