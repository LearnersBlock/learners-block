import config
import os
from common.models import User
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


# Change default logging mode when in development environmnets
if "BALENA_APP_NAME" in os.environ and \
        os.environ['BALENA_APP_NAME'].lower() == "lb-dev":
    dev_mode = True
elif os.environ['FLASK_ENV'].lower() == "development":
    dev_mode = True
else:
    dev_mode = False


class settings_get_ui(Resource):
    def get(self):
        lb_database = User.query.filter_by(username=config.default_hostname
                                           ).first()

        # Check if there is a wifi password set and return boolean
        if lb_database.wifi_password:
            wifi_password = True
        else:
            wifi_password = False

        return {'files': lb_database.files,
                'library': lb_database.library,
                'website': lb_database.website,
                'start_page': lb_database.start_page,
                'wifi_password_set': wifi_password,
                'dev_mode': dev_mode}


class settings_set_ui(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # Fetch current settings toggle and field status
        lb_database = User.query.filter_by(username=config.default_hostname
                                           ).first()

        for key, value in content.items():
            setattr(lb_database, key, value)

        lb_database.save_to_db()

        return {'message': 'done'}
