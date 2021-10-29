import atexit
import config
import os
import signal
import subprocess
from common.errors import errors
from common.errors import logger
from common.models import db
from common.models import migrate
from common.processes import curl
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restful import Api as _Api
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import PyJWTError
from resources.docker_routes import docker_image
from resources.docker_routes import docker_pull
from resources.docker_routes import docker_remove
from resources.docker_routes import docker_run
from resources.download_routes import download_fetch
from resources.download_routes import download_stop
from resources.download_routes import download_stream
from resources.filemanager_routes import filemanager_copy
from resources.filemanager_routes import filemanager_delete
from resources.filemanager_routes import filemanager_file_size
from resources.filemanager_routes import filemanager_list
from resources.filemanager_routes import filemanager_move
from resources.filemanager_routes import filemanager_newfolder
from resources.filemanager_routes import filemanager_rename
from resources.filemanager_routes import filemanager_unzip
from resources.filemanager_routes import filemanager_upload
from resources.system_routes import system_health_check
from resources.system_routes import system_info
from resources.system_routes import system_portainer
from resources.system_routes import system_prune
from resources.system_routes import system_reset_database


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

    # Import app context from config file
    app.config.from_object(config.context)

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
    # Set PID file for monitoring whether there has already been a first boot
    pidfile = "/app/db/run.pid"

    pid = str(os.getpid())

    container_hostname = subprocess.run(["hostname"],
                                        capture_output=True,
                                        check=True,
                                        text=True).stdout.rstrip()
    if not os.path.isfile(pidfile):
        # Run tasks on first launch
        # Set hostname to default
        open(pidfile, 'w').write(pid)

        logger.info('Created first launch PID.')

        if container_hostname != config.default_hostname:
            curl(method="patch",
                 path="/v1/device/host-config?apikey=",
                 string='{"network": {"hostname": "%s"}}' %
                 (config.default_hostname),
                 supervisor_retries=20)

            logger.info('Set hostname on first boot. Restarting.')

            curl(method="post-json",
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
        from resources.app_store_routes import appstore_get_apps, \
            appstore_status
        from resources.auth_routes import auth_log_in, auth_log_out, \
            auth_set_password, auth_verify_login, \
            auth_verify_user_password_state
        from resources.settings_routes import settings_get_ui, \
            settings_set_ui

        init_database()

    # Load and launch based on dev or prod mode
    if os.environ['FLASK_ENV'].lower() == "production":
        # Import production routes
        from boot.production import handle_exit, handle_sigterm, startup
        from resources.system_routes import system_hostname
        from resources.supervisor_routes import supervisor_device, \
            supervisor_host_config, supervisor_journal_logs, \
            supervisor_update, supervisor_uuid
        from resources.wifi_routes import wifi_connect, \
            wifi_connection_status, wifi_forget, wifi_forget_all, \
            wifi_list_access_points, wifi_set_password, wifi_set_ssid

        logger.info("Api-v1 - Starting API (Production)...")

        # Ensure soft shutdown to terminate wifi-connect
        atexit.register(handle_exit, None, None)
        signal.signal(signal.SIGHUP, handle_sigterm)
        signal.signal(signal.SIGINT, handle_sigterm)
        signal.signal(signal.SIGTERM, handle_sigterm)

        # Check if first launch
        try:
            first_launch()
        except Exception:
            logger.error('Error in first launch boot process.')
            # Continuing to allow boot for debugging.

        # Execute startup processes
        try:
            startup()
        except Exception:
            logger.exception('Fail on startup.')
            # Allowing API to still come up for debugging
    else:
        # Import development routes
        from resources.dev_routes import supervisor_device, \
            supervisor_host_config, supervisor_journal_logs, \
            supervisor_update, supervisor_uuid, system_hostname, \
            wifi_connect, wifi_connection_status, wifi_forget, \
            wifi_forget_all, wifi_list_access_points, wifi_set_password, \
            wifi_set_ssid

        logger.info("Api-v1 - Starting API (Development)...")

    # Configure endpoints #

    # App Store
    api.add_resource(appstore_get_apps, '/v1/appstore/get_apps')
    api.add_resource(appstore_status, '/v1/appstore/status')

    # Auth
    api.add_resource(auth_log_in, '/v1/auth/log_in')
    api.add_resource(auth_log_out, '/v1/auth/log_out')
    api.add_resource(auth_set_password, '/v1/auth/set_password')
    api.add_resource(auth_verify_login, '/v1/auth/verify_login')
    api.add_resource(auth_verify_user_password_state,
                     '/v1/auth/verify_user_password_state')

    # Docker
    api.add_resource(docker_image, '/v1/docker/image')
    api.add_resource(docker_pull, '/v1/docker/pull')
    api.add_resource(docker_remove, '/v1/docker/remove')
    api.add_resource(docker_run, '/v1/docker/run')

    # Download
    api.add_resource(download_fetch, '/v1/download/fetch')
    api.add_resource(download_stop, '/v1/download/stop')
    api.add_resource(download_stream, '/v1/download/stream')

    # Filemanager
    api.add_resource(filemanager_copy, '/v1/filemanager/copy')
    api.add_resource(filemanager_delete, '/v1/filemanager/delete')
    api.add_resource(filemanager_file_size, '/v1/filemanager/file_size')
    api.add_resource(filemanager_list, '/v1/filemanager/list')
    api.add_resource(filemanager_move, '/v1/filemanager/move')
    api.add_resource(filemanager_newfolder, '/v1/filemanager/new_folder')
    api.add_resource(filemanager_rename, '/v1/filemanager/rename')
    api.add_resource(filemanager_unzip, '/v1/filemanager/unzip')
    api.add_resource(filemanager_upload, '/v1/filemanager/upload')

    # Settings
    api.add_resource(settings_get_ui, '/v1/settings/get_ui')
    api.add_resource(settings_set_ui, '/v1/settings/set_ui')

    # Supervisor
    api.add_resource(supervisor_device, '/v1/supervisor/device')
    api.add_resource(supervisor_host_config, '/v1/supervisor/host_config')
    api.add_resource(supervisor_journal_logs, '/v1/supervisor/journal_logs')
    api.add_resource(supervisor_update, '/v1/supervisor/update')
    api.add_resource(supervisor_uuid, '/v1/supervisor/uuid')

    # System
    api.add_resource(system_health_check, '/')
    api.add_resource(system_hostname, '/v1/system/hostname')
    api.add_resource(system_info, '/v1/system/info')
    api.add_resource(system_portainer, '/v1/system/portainer')
    api.add_resource(system_prune, '/v1/system/prune')
    api.add_resource(system_reset_database, '/v1/system/reset_database')

    # Wi-Fi
    api.add_resource(wifi_connect, '/v1/wifi/connect')
    api.add_resource(wifi_connection_status, '/v1/wifi/connection_status')
    api.add_resource(wifi_forget, '/v1/wifi/forget')
    api.add_resource(wifi_forget_all, '/v1/wifi/forget_all')
    api.add_resource(wifi_list_access_points, '/v1/wifi/list_access_points')
    api.add_resource(wifi_set_password, '/v1/wifi/set_password')
    api.add_resource(wifi_set_ssid, '/v1/wifi/set_ssid')

    # Initialise and start
    api.init_app(app)

    app.run(port=9090, host='0.0.0.0')
