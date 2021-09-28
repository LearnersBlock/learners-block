from common.models import User
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class set_ui(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # Fetch current settings toggle and field status
        lb_database = User.query.filter_by(username='lb').first()

        if "files" in content:
            if content["files"].lower() == "true":
                lb_database.files = True
            else:
                lb_database.files = False
        if "library" in content:
            if content["library"].lower() == "true":
                lb_database.library = True
            else:
                lb_database.library = False
        if "website" in content:
            if content["website"].lower() == "true":
                lb_database.website = True
            else:
                lb_database.website = False
        if "start_page" in content:
            lb_database.start_page = content["start_page"]

        lb_database.save_to_db()

        return {'message': 'done'}, 200


class settings_ui(Resource):
    def get(self):
        lb_database = User.query.filter_by(username='lb').first()

        # Check if there is a wifi password set and return boolean
        if lb_database.wifi_password:
            wifi_password = True
        else:
            wifi_password = False

        return {'files': lb_database.files,
                'library': lb_database.library,
                'website': lb_database.website,
                'start_page': lb_database.start_page,
                'wifi_password_set': wifi_password}, 200
