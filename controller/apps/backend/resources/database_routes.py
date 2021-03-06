from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from resources.models import User


class set_ui(Resource):
    @jwt_required()
    def post(self):
        try:
            lb_database = User.query.filter_by(username='lb').first()
        except Exception as ex:
            print(self.__class__.__name__ + " - " + str(ex))
            return {'response': self.__class__.__name__ + " - " + str(ex)}, 403

        try:
            content = request.get_json()
        except AttributeError as ex:
            print(self.__class__.__name__ + " - " + str(ex))
            return {'response': 'Error: Must pass valid string.'}, 403

        try:
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
            return {'response': 'done'}, 200
        except Exception as ex:
            print(self.__class__.__name__ + " - " + str(ex))
            return {'message': self.__class__.__name__ + " - " + str(ex)}, 500


class settings_ui(Resource):
    def get(self):
        lb_database = User.query.filter_by(username='lb').first()
        return {'files': lb_database.files,
                'library': lb_database.library,
                'website': lb_database.website,
                'start_page': lb_database.start_page}, 200
