from common.models import db
from common.models import migrate
from common.system_processes import curl
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restful import Api as _Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import PyJWTError
from resources.docker_routes import docker_pull
from resources.docker_routes import docker_remove
from resources.docker_routes import docker_run
from resources.download_routes import download_fetch
from resources.download_routes import download_stop
from resources.download_routes import download_stream
from resources.errors import errors
from resources.errors import print_message
from resources.filemanager_routes import filemanager_copy
from resources.filemanager_routes import filemanager_delete
from resources.filemanager_routes import filemanager_file_size
from resources.filemanager_routes import filemanager_list
from resources.filemanager_routes import filemanager_move
from resources.filemanager_routes import filemanager_newfolder
from resources.filemanager_routes import filemanager_rename
from resources.filemanager_routes import filemanager_unzip
from resources.filemanager_routes import filemanager_upload
from resources.system_routes import health_check
from resources.system_routes import internet_connection_status
from resources.system_routes import system_info
from resources.system_routes import system_prune
import atexit
import os
import signal
import subprocess


# Apply fix to Flask-Restful not aligned with JWT exceptions
# https://github.com/flask-restful/flask-restful/issues/783#issuecomment-570177004
class Api(_Api):
    def error_router(self, original_handler, e):
        if not isinstance(e, PyJWTError) \
            and not isinstance(e, JWTExtendedException) \
                and self._has_fr_route():
            try:
                return self.handle_error(e)
            except Exception:
                pass  # Fall through to original handler
        return original_handler(e)


# Import .env file to make env vars available from os.environ
load_dotenv()

# Load extensions
jwt = JWTManager()

# Load Flask-Restful API
api = Api(errors=errors)


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


# Check if first launch
def first_launch():
    # Check first launch PID
    pid = str(os.getpid())
    pidfile = "/app/db/run.pid"
    container_hostname = subprocess.run(["hostname"],
                                        capture_output=True,
                                        check=True,
                                        text=True).stdout.rstrip()
    if not os.path.isfile(pidfile):
        # Run tasks on first launch
        # Set hostname to 'lb'
        open(pidfile, 'w').write(pid)

        print_message('first_launch',
                      'Created first launch PID.')

        if container_hostname != 'lb':
            response = curl(method="patch",
                            path="/v1/device/host-config?apikey=",
                            string='{"network": {"hostname": "lb"}}',
                            supervisor_retries=20)

            print_message('first_launch',
                          'Set hostname on first boot. Restarting',
                          str(response))

            response = curl(method="post-json",
                            path="/v1/reboot?apikey=",
                            string='("force", "true")',
                            supervisor_retries=20)


# Create Flask app instance
app = create_app()


# Startup process
if __name__ == '__main__':
    # Initialise database
    with app.app_context():
        from common.models import init_database
        from resources.app_store_routes import app_store_set, \
            app_store_status
        from resources.auth_routes import login, logout, set_password, \
            verify_login
        from resources.settings_routes import set_ui, \
            settings_ui

        init_database()

    # Load and launch based on dev or prod mode
    if os.environ['FLASK_ENV'].lower() == "production":
        from boot.production import handle_exit, handle_sigterm, startup
        from resources.system_routes import hostname
        from resources.supervisor_routes import container_start, \
            container_status, container_stop, device, host_config, \
            journal_logs, update, uuid
        from resources.wifi_routes import set_wifi, wifi_connect, \
            wifi_connection_status, wifi_forget, wifi_forget_all, \
            wifi_list_access_points

        print("Api-v1 - Starting API (Production)...")

        # Ensure soft shutdown to term wifi-connect
        atexit.register(handle_exit, None, None)
        signal.signal(signal.SIGHUP, handle_sigterm)
        signal.signal(signal.SIGINT, handle_sigterm)
        signal.signal(signal.SIGTERM, handle_sigterm)

        # Check if first launch
        first_launch()

        # Execute startup processes
        try:
            startup()
        except Exception as ex:
            print_message('__name__', 'Fail on startup.', ex)
    else:
        from resources.dev_routes import container_start, container_status, \
             container_stop, device, host_config, hostname, journal_logs, \
             set_wifi, update, uuid, wifi_connect, wifi_connection_status, \
             wifi_forget, wifi_forget_all, wifi_list_access_points

        print("Api-v1 - Starting API (Development)...")

    # Configure endpoints
    api.add_resource(app_store_set, '/v1/appstore/set')
    api.add_resource(app_store_status, '/v1/appstore/status')
    api.add_resource(container_start, '/v1/container/start')
    api.add_resource(container_status, '/v1/container/status')
    api.add_resource(container_stop, '/v1/container/stop')
    api.add_resource(device, '/v1/device')
    api.add_resource(docker_pull, '/v1/docker/pull')
    api.add_resource(docker_remove, '/v1/docker/remove')
    api.add_resource(docker_run, '/v1/docker/run')
    api.add_resource(download_fetch, '/v1/download/fetch')
    api.add_resource(download_stop, '/v1/download/stop')
    api.add_resource(download_stream, '/v1/download/stream')
    api.add_resource(filemanager_copy, '/v1/filemanager/copy')
    api.add_resource(filemanager_delete, '/v1/filemanager/delete')
    api.add_resource(filemanager_file_size, '/v1/filemanager/file_size')
    api.add_resource(filemanager_list, '/v1/filemanager/list')
    api.add_resource(filemanager_move, '/v1/filemanager/move')
    api.add_resource(filemanager_newfolder, '/v1/filemanager/newfolder')
    api.add_resource(filemanager_rename, '/v1/filemanager/rename')
    api.add_resource(filemanager_unzip, '/v1/filemanager/unzip')
    api.add_resource(filemanager_upload, '/v1/filemanager/upload')
    api.add_resource(health_check, '/')
    api.add_resource(host_config, '/v1/hostconfig')
    api.add_resource(hostname, '/v1/hostname')
    api.add_resource(internet_connection_status,
                     '/v1/internet/connectionstatus')
    api.add_resource(journal_logs, '/v1/journallogs')
    api.add_resource(login, '/v1/login')
    api.add_resource(logout, '/v1/logout')
    api.add_resource(set_password, '/v1/setpassword')
    api.add_resource(settings_ui, '/v1/settingsui')
    api.add_resource(set_ui, '/v1/setui')
    api.add_resource(set_wifi, '/v1/setwifi')
    api.add_resource(system_info, '/v1/system/info')
    api.add_resource(system_prune, '/v1/system/prune')
    api.add_resource(update, '/v1/update')
    api.add_resource(uuid, '/v1/uuid')
    api.add_resource(verify_login, '/v1/verifylogin')
    api.add_resource(wifi_connect, '/v1/wifi/connect')
    api.add_resource(wifi_connection_status, '/v1/wifi/connectionstatus')
    api.add_resource(wifi_forget, '/v1/wifi/forget')
    api.add_resource(wifi_forget_all, '/v1/wifi/forgetall')
    api.add_resource(wifi_list_access_points, '/v1/wifi/networks')

    api.init_app(app)

    app.run(port=9090, host='0.0.0.0')
