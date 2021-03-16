from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from resources.models import User


class set_ui(Resource):
    @jwt_required()
    def post(self):
        try:
            lb_database = User.query.filter_by(username='lb').first()
        except:
            return {'response': 'Error reading database.'}, 403

        try:
            content = request.get_json()
        except AttributeError:
            return {'response': 'Error: Must pass valid string.'}, 403

        try:
            if "files" in content:
                if content["files"].lower() == "true":
                    lb_database.files = True
                elif content["files"].lower() == "false":
                    lb_database.files = False
            if "library" in content:
                if content["library"].lower() == "true":
                    lb_database.library = True
                elif content["library"].lower() == "false":
                    lb_database.library = False
            if "makerspace" in content:
                if content["makerspace"].lower() == "true":
                    lb_database.makerspace = True
                elif content["makerspace"].lower() == "false":
                    lb_database.makerspace = False
            if "website" in content:
                if content["website"].lower() == "true":
                    lb_database.website = True
                elif content["website"].lower() == "false":
                    lb_database.website = False

            lb_database.save_to_db()
            return {'response': 'done'}, 200
        except:
            return {'message': 'Something went wrong saving to '
                    'the database'}, 500


class settings_ui(Resource):
    def get(self):
        lb_database = User.query.filter_by(username='lb').first()
        return {'files': lb_database.files,
                'library': lb_database.library,
                'makerspace': lb_database.makerspace,
                'website': lb_database.website}, 200