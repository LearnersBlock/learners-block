import config
from common.models import User
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
    except (RuntimeError, KeyError):
        # If there is not a valid JWT return the original respone
        return response

    return response


class auth_log_in(Resource):
    def post(self):
        content = request.get_json()

        lb_database = User.query.filter_by(username=config.default_hostname
                                           ).first()
        verify_password = User.verify_password(content["password"],
                                               lb_database.password)

        username = content["username"].lower()

        if username != lb_database.username or verify_password is not \
                True:
            return {"message": "Invalid username or password"}, 401
        access_token = create_access_token(identity=username)
        response = jsonify({"message": "login successful",
                            "token": access_token})
        set_access_cookies(response, access_token)

        return response


class auth_log_out(Resource):
    def post(self):
        response = jsonify({"message": "logout successful"})
        unset_jwt_cookies(response)
        return response


class auth_set_password(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        lb_database = User.query.filter_by(username=config.default_hostname
                                           ).first()
        hashed_password = User.hash_password(content["password"])
        lb_database.password = hashed_password
        lb_database.save_to_db()

        return {'message': 'done'}


class auth_verify_login(Resource):
    def get(self):
        try:
            verify_jwt_in_request()
        except Exception:
            return {'logged_in': False}

        # Return logged in status and identity
        return {'logged_in': True, 'user': get_jwt_identity()}


class auth_verify_user_password_state(Resource):
    def get(self):
        lb_database = User.query.filter_by(username=config.default_hostname
                                           ).first()

        # Check if there is a user password set
        verified_password = User.verify_password(' ',
                                                 lb_database.password)

        return {'default_login_password_set': not verified_password}
