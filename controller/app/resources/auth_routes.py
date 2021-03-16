from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask import current_app
from flask import jsonify
from flask import request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import verify_jwt_in_request
from flask_restful import Resource
from resources.models import User


# Refresh token on each authorised request
@current_app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


class login(Resource):
    def post(self):
        try:
            lb_database = User.query.filter_by(username='lb').first()
        except Exception as ex:
            return {'response': str(ex)}, 500

        try:
            content = request.get_json()
            verify_password = User.verify_password(content["password"],
                                                   lb_database.password)
            username = content["username"].lower()
        except AttributeError:
            return {'response': 'Error: Must pass valid string.'}, 200

        if username != lb_database.username or verify_password is not \
                True:
            return {"message": "Bad username or password"}, 200
        access_token = create_access_token(identity=username)
        response = jsonify({"message": "login successful",
                            "token": access_token})
        set_access_cookies(response, access_token)

        return response


class logout(Resource):
    def post(self):
        response = jsonify({"message": "logout successful"})
        unset_jwt_cookies(response)
        return response


class set_password(Resource):
    @jwt_required()
    def post(self):
        try:
            lb_database = User.query.filter_by(username='lb').first()
        except Exception as ex:
            return {'response': str(ex)}, 403

        try:
            content = request.get_json()
        except AttributeError:
            return {'response': 'Error: Must pass valid string.'}, 403

        try:
            hashed_password = User.hash_password(content["password"])
            lb_database.password = hashed_password
            lb_database.save_to_db()
            return {'response': 'done'}, 200
        except Exception as ex:
            return {'message': str(ex)}, 500


class verify_login(Resource):
    def get(self):
        try:
            verify_jwt_in_request()
            return {'logged_in': True, 'user': get_jwt_identity()}, 200
        except Exception:
            return {'logged_in': False}, 200
