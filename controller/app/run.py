from common.processes import database_recover
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.models import db
from resources.models import migrate
from resources.system_routes import health_check
from resources.system_routes import rsync_fetch
from resources.system_routes import rsync_stop
from resources.system_routes import system_info
import atexit
import os
import signal
import subprocess
import threading
import time

# Import .env file
load_dotenv()


# Create Flask app instance and required databases
def create_app(config):
    # Initalise and configure Flask
    app = Flask(__name__)
    app.config.from_object(config)

    # Allow CORS
    CORS(app)

    # Setup Flask-JWT-Extended
    jwt = JWTManager(app)

    # Import database and migration process

    db.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)
    return app, api, jwt


# Function for first launch called by 'startup' function
def launch(self):
    # Check if already connected to Wi-Fi
    time.sleep(20)
    try:
        connected = wifi().check_connection()
    except Exception as ex:
        print("Api-v1 - Error checking wifi connection. Starting wifi-connect "
              "in order to allow debugging. " + str(ex))
        connected = None

    # If connected, perform container updatem if not, start Wi-Fi Connect
    if connected:
        try:
            update().get()
            response = ('Api-v1 - API Started - Device already connected to '
                        'local wifi, software update request made.')
        except Exception as ex:
            response = "Software update failed. " + str(ex)
    else:
        try:
            wifi_connect().start()
            response = "Api-v1 - API Started - Launched wifi-connect."
        except Exception as ex:
            response = "Wifi-connect failed to launch. " + str(ex)

    print(response)
    return response


def hostname_check(self):
    # Check hostname in container is correct
    try:
        # Fetch container hostname and device hostname
        container_hostname = subprocess.run(["hostname"], capture_output=True,
                                            text=True).stdout.rstrip()

        device_hostname = curl(method="get",
                               path="/v1/device/host-config?apikey=",
                               supervisor_retries=20)

        # Check container and device hostname match
        if container_hostname != \
                device_hostname["json_response"]["network"]["hostname"]:
            print("Api-v1 - Container hostname and device hostname do not "
                  "match. Likely a hostname change has been performed. Balena "
                  "Supervisor should detect this and rebuild the container "
                  "shortly. Waiting 60 seconds before continuing anyway.")
            time.sleep(60)

    except Exception as ex:
        print("Api-v1 - Failed to compare hostnames, starting anyway: "
              + str(ex))


def portainer_check(self):
    # Stop portainer on boot
    # String cannot be portainer_stop due to clash with endpoint
    try:
        portainer_exit = threading.Thread(target=container.stop,
                                          args=(None, "portainer", 10),
                                          name='portainer_exit')
        portainer_exit.start()

    except Exception as ex:
        print("Failed to stop Portainer. " + str(ex))


def startup(self):
    # If connected to a wifi network then update device,
    # otherwise launch wifi-connect
    try:
        device_start = threading.Thread(target=launch,
                                        args=(1,),
                                        name='device_start')
        device_start.start()

    except Exception as ex:
        print("Failed during launch. Continuing for debug. " + str(ex))


# Including initial app build here as database migration will not work when
# under __name__

if os.environ['FLASK_ENV'].lower() == "production":
    app, api, jwt = create_app('config.Production')
else:
    app, api, jwt = create_app('config.Development')

# Import files reliant on Flask App having been built
with app.app_context():
    from resources.auth_routes import login, logout, set_password, verify_login
    from resources.database_routes import set_ui, settings_ui


# Startup process
if __name__ == '__main__':
    from resources.models import create_default_user
    try:
        with app.app_context():
            db.create_all()
            create_default_user()
    except Exception as ex:
        print("Database error. Trying to recover: " + str(ex))
        database_recover()

    # Load and launch based on dev or prod mode
    if os.environ['FLASK_ENV'].lower() == "production":
        print("Api-v1 - Starting API (Production)...")
        from common.processes import curl
        from common.containers import container
        from common.processes import handle_exit
        from common.wifi import wifi
        from common.wifi import wifi_connect
        from resources.system_routes import hostname
        from resources.supervisor_routes import device, host_config, \
            journal_logs, portainer_status, portainer_start, portainer_stop, \
            update, uuid
        from resources.wifi_routes import wifi_connection_status, \
            wifi_forget, wifi_forget_all

        # Ensure soft shutdown to term wifi-connect
        atexit.register(handle_exit, None, None)
        signal.signal(signal.SIGTERM, handle_exit)
        signal.signal(signal.SIGINT, handle_exit)

        # Check portainer status on boot
        portainer_check(None)

        # Check hostnames are set correctly
        hostname_check(None)

        # Start app
        startup(None)

    else:
        print("Api-v1 - Starting API (Development)...")
        from resources.dev_routes import device, host_config, hostname, \
            journal_logs, portainer_status, portainer_start, portainer_stop, \
            update, uuid, wifi_connection_status, wifi_forget, wifi_forget_all

    # Configure endpoints
    api.add_resource(device, '/v1/device')
    api.add_resource(health_check, '/')
    api.add_resource(host_config, '/v1/hostconfig')
    api.add_resource(hostname, '/v1/hostname')
    api.add_resource(journal_logs, '/v1/journallogs')
    api.add_resource(login, '/v1/login')
    api.add_resource(logout, '/v1/logout')
    api.add_resource(portainer_status, '/v1/portainer/status')
    api.add_resource(portainer_start, '/v1/portainer/start')
    api.add_resource(portainer_stop, '/v1/portainer/stop')
    api.add_resource(rsync_fetch, '/v1/rsync/fetch')
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

    app.run(port=9090, host='0.0.0.0')
