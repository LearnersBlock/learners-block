import os
import secrets
from datetime import timedelta
from dotenv import dotenv_values

# Access point names
ap_name = 'LBNETWORK'
hotspot_name = 'HOTSPOT'

# Default values
default_ssid = "Learner's Block"
default_hostname = 'lb'

# Set dev env variables
if "BALENA_APP_NAME" in os.environ and \
        os.environ['BALENA_APP_NAME'].lower() == "lb-dev":
    dev_mode = True
elif os.environ['FLASK_ENV'].lower() == "development":
    dev_mode = True
else:
    dev_mode = False

# Wi-Fi modes
type_hotspot = 'HOTSPOT'
type_none = 'NONE'
type_wep = 'WEP'
type_wpa = 'WPA'
type_wpa2 = 'WPA2'
type_enterprise = 'ENTERPRISE'


# Fetch the secret key or generate one if it is absent
def get_secret_key():
    # Generate secret key
    if not dotenv_values("db/.secret_key"):
        with open('./db/.secret_key', 'w') as secrets_file:
            secrets_file.write("SECRET_KEY = " + secrets.token_hex(32))
    key = dotenv_values("./db/.secret_key")
    return key["SECRET_KEY"]


# App context object for importing in to Flask
class context:
    # JWT Auth
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_SECURE = False
    JWT_SECRET_KEY = get_secret_key()
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    PROPAGATE_EXCEPTIONS = False

    # CORS
    CORS_SUPPORTS_CREDENTIALS = True

    # Database variables
    SQLALCHEMY_DATABASE_URI = "sqlite:///db/sqlite.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
