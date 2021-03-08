from dotenv import load_dotenv
from datetime import timedelta
from dotenv import dotenv_values
import os
import secrets

# Import .env file
load_dotenv()


# Fetch secret key of generate if absent
def get_secret_key():
    # Generate secret key
    if not dotenv_values("db/.secret_key"):
        with open('./db/.secret_key', 'w') as secret_file:
            secret_file.write("SECRET_KEY = " + secrets.token_hex(32))
    key = dotenv_values("./db/.secret_key")
    return key["SECRET_KEY"]


# Development configuration
class Development:
    if os.environ['FLASK_ENV'].lower != "production":
        # Flask variables #
        # JWT Auth
        JWT_TOKEN_LOCATION = ["headers", "cookies"]
        JWT_COOKIE_SECURE = False
        JWT_SECRET_KEY = get_secret_key()
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
        # Database variables
        PROPAGATE_EXCEPTIONS = True
        SQLALCHEMY_DATABASE_URI = "sqlite:///db/sqlite.db"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        # Set below to False to prevent needing to pass additional header
        # JWT_COOKIE_CSRF_PROTECT = False


# Production configuration
class Production:
    if os.environ['FLASK_ENV'].lower == "production":
        # JWT Auth
        JWT_TOKEN_LOCATION = ["headers", "cookies"]
        JWT_COOKIE_SECURE = False
        JWT_SECRET_KEY = get_secret_key()
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

        # Database variables
        PROPAGATE_EXCEPTIONS = True
        SQLALCHEMY_DATABASE_URI = "sqlite:///db/sqlite.db"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
