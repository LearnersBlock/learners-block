import config
from common.models import User
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class settings_default_startpage(Resource):
    def get(self):
        lb_database = User.query.filter_by(
            username=config.default_hostname
        ).first()
        return {"start_page": lb_database.start_page}


class settings_get_ui(Resource):
    def get(self):
        lb_database = User.query.filter_by(
            username=config.default_hostname
        ).first()
        return {
            "files": lb_database.files,
            "library": lb_database.library,
            "website": lb_database.website,
            "dev_mode": config.dev_mode,
        }


class settings_set_ui(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # Fetch current settings toggle and field status
        lb_database = User.query.filter_by(
            username=config.default_hostname
        ).first()

        for key, value in content.items():
            setattr(lb_database, key, value)

        lb_database.save_to_db()

        return {"message": "done"}
