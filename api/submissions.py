from flask import *
from api.lib.db import *

api_submissions = Blueprint('api_submissions', __name__, template_folder='templates')


@api_submissions.route('/api-<api_token>/submissions', methods=['GET'])
def submission_api(api_token):
    if api_token == 'test':
        data = return_all_activities()
        resp = jsonify(data)

        return resp
    else:
        return jsonify({'error_message': 'Your token is invalid.'})


@api_submissions.route('/api-<api_token>/submissions/<id>', methods=['GET'])
def submission_api_by_id(api_token, id):
    if api_token == 'test':
        try:
            data = return_all_activities()[int(id)]
            to_send = {id: data}
            resp = jsonify(to_send)

            return resp
        except Exception as e:
            return jsonify({'error_message': str(e)})
    else:
        return jsonify({'error_message': 'Your token is invalid.'})
