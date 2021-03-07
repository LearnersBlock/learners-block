import secrets  #
from dotenv import dotenv_values


def get_secret_key():
    # Generate secret key
    if not dotenv_values("db/.secret_key"):
        with open('./db/.secret_key', 'w') as secret_file:
            secret_file.write("SECRET_KEY = " + secrets.token_hex(32))
    key = dotenv_values("./db/.secret_key")
    return key["SECRET_KEY"]


class Development:
    CORS_EXPOSE_HEADERS = 'Access-Token'
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_SECURE = False
    JWT_SECRET_KEY = get_secret_key()
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/sqlite.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Set below to False to prevent needing to pass additional header
    # JWT_COOKIE_CSRF_PROTECT = False
