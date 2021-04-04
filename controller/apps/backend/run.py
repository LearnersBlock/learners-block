from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.models import db
from resources.models import migrate
from resources.system_routes import health_check
from resources.system_routes import internet_connection_status
from resources.system_routes import rsync_fetch
from resources.system_routes import rsync_status
from resources.system_routes import rsync_stop
from resources.system_routes import system_info
import atexit
import inspect
import os
import signal

# Import .env file
load_dotenv()

# Load extensions
jwt = JWTManager()
api = Api()


# Create Flask app instance
def create_app():
    # Initalise and configure Flask
    app = Flask(__name__)

    # Import relevant config
    if os.environ['FLASK_ENV'].lower() == "production":
        from config import Production
        app.config.from_object(Production)
    else:
        from config import Development
        app.config.from_object(Development)

    # Allow CORS
    CORS(app)

    # Setup Flask-JWT-Extended
    jwt.init_app(app)

    # Import database and migration process
    db.init_app(app)
    migrate.init_app(app, db)

    return app


app = create_app()


# Startup process
if __name__ == '__main__':
    # Initialise database
    with app.app_context():
        from resources.auth_routes import login, logout, set_password, \
             verify_login
        from resources.database_routes import set_ui, settings_ui
        from resources.models import init_database

        init_database()

    # Load and launch based on dev or prod mode
    if os.environ['FLASK_ENV'].lower() == "production":
        from boot.production import startup
        from common.wifi import handle_exit
        from resources.system_routes import hostname
        from resources.supervisor_routes import device, host_config, \
            journal_logs, portainer_status, portainer_start, portainer_stop, \
            update, uuid
        from resources.wifi_routes import wifi_connection_status, \
            wifi_forget, wifi_forget_all

        print("Api-v1 - Starting API (Production)...")

        # Ensure soft shutdown to term wifi-connect
        atexit.register(handle_exit, None, None)
        signal.signal(signal.SIGTERM, handle_exit)
        signal.signal(signal.SIGINT, handle_exit)
        signal.signal(signal.SIGHUP, handle_exit)

        # Execute startup processes
        try:
            startup()
        except Exception as ex:
            print("Failed on boot. " +
                  inspect.stack()[0][3] + " - " + str(ex))

    else:
        from resources.dev_routes import device, host_config, hostname, \
            journal_logs, portainer_status, portainer_start, portainer_stop, \
            update, uuid, wifi_connection_status, wifi_forget, wifi_forget_all

        print("Api-v1 - Starting API (Development)...")

    # Configure endpoints
    api.add_resource(device, '/v1/device')
    api.add_resource(health_check, '/')
    api.add_resource(host_config, '/v1/hostconfig')
    api.add_resource(hostname, '/v1/hostname')
    api.add_resource(internet_connection_status,
                     '/v1/internet/connectionstatus')
    api.add_resource(journal_logs, '/v1/journallogs')
    api.add_resource(login, '/v1/login')
    api.add_resource(logout, '/v1/logout')
    api.add_resource(portainer_status, '/v1/portainer/status')
    api.add_resource(portainer_start, '/v1/portainer/start')
    api.add_resource(portainer_stop, '/v1/portainer/stop')
    api.add_resource(rsync_fetch, '/v1/rsync/fetch')
    api.add_resource(rsync_status, '/v1/rsync/status')
    api.add_resource(rsync_stop, '/v1/rsync/stop')
    api.add_resource(set_password, '/v1/setpassword')
    api.add_resource(settings_ui, '/v1/settingsui')
    api.add_resource(set_ui, '/v1/setui')
    api.add_resource(system_info, '/v1/system/info')
    api.add_resource(update, '/v1/update')
    api.add_resource(uuid, '/v1/uuid')
    api.add_resource(verify_login, '/v1/verifylogin')
    api.add_resource(wifi_connection_status, '/v1/wifi/connectionstatus')
    api.add_resource(wifi_forget, '/v1/wifi/forget')
    api.add_resource(wifi_forget_all, '/v1/wifi/forgetall')

    api.init_app(app)

    app.run(port=9090, host='0.0.0.0')
