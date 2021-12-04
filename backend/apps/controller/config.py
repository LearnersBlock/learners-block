import os
import secrets
from datetime import timedelta
from dotenv import dotenv_values
from dotenv import load_dotenv

# Import .env file to make those env vars available from os.environ.
# Vars imported from .env are overridden by local envs.
load_dotenv()

# Access point names
ap_name = 'LBNETWORK'
hotspot_name = 'HOTSPOT'

# Default values
default_ssid = "Learner's Block"
default_hostname = 'lb'

# If the device is running on Balena set the Docker socket
if "BALENA_HOST_OS_VERSION" in os.environ:
    socket_path = '/var/run/balena-engine.sock'
else:
    socket_path = '/var/run/docker.sock'

# Set dev env variables
if "FLASK_ENV" in os.environ and \
        os.environ['FLASK_ENV'].lower() == "development":
    dev_mode = True
else:
    dev_mode = False

# Change default logging mode when in development environmnets
dev_device = False
if ("BALENA_APP_NAME" in os.environ and
   os.environ['BALENA_APP_NAME'].lower() == "lb-dev"):
    dev_device = True

# Store the chronyd state to avoid polling multiple times
chronyd_synced = False

# Default access point name. No need to change these under usual operation as
# they are for use inside the app only. PWC is acronym for 'Py Wi-Fi Connect'.
ap_name = 'PWC'

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
