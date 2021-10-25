from common.processes import get_secret_key
from datetime import timedelta

# Access point names
ap_name = 'LBNETWORK'
hotspot_name = 'HOTSPOT'

# Default values
default_ssid = "Learner's Block"
default_hostname = 'lb'

# Wi-Fi modes
type_hotspot = 'HOTSPOT'
type_none = 'NONE'
type_wep = 'WEP'
type_wpa = 'WPA'
type_wpa2 = 'WPA2'
type_enterprise = 'ENTERPRISE'


# App ontext object for importing in to Flask
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
