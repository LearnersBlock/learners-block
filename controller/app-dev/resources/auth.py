from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask import current_app
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies


@current_app.after_request()
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
