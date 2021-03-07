from flask_restful import Resource
from flask import jsonify  #
from flask import request  #
from werkzeug import serving
from dotenv import dotenv_values
##
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import verify_jwt_in_request
from resources.models import User
import subprocess

##
import os
import shutil
import time

# Set default Wi-Fi status for mock endpoint
wifistatus = False
portainerstatus = False

# Load Python library for managing enviroment variables
env_variables = dotenv_values(".env")

# Import software version number
VER = os.getenv('VER')

# Disable logging for health check
parent_log_request = serving.WSGIRequestHandler.log_request


# Prevents access logging when running healthcheck on /
def log_request(self, *args, **kwargs):
    if self.path == '/':
        return

    parent_log_request(self, *args, **kwargs)


# Calculate the space remaining for the settings panel
def humansize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


class device(Resource):
    def get(self):
        return {'response': 'output'}, 200


class health_check(Resource):
    def get(self):
        serving.WSGIRequestHandler.log_request = log_request
        return {'status': 200, 'message': 'ok'}, 200


class host_config(Resource):
    @jwt_required()
    def get(self, hostname):

        return {
            'status': 200,
            'message': f'Hostname was updated to {hostname}'
        }, 200


class hostname(Resource):
    def get(self):
        container_hostname = subprocess.run(["hostname"], capture_output=True,
                                            text=True).stdout.rstrip()
        return {
            'status': 200,
            'hostname': container_hostname
        }, 200


class journal_logs(Resource):
    def get(self):

        return "journal logs"


class login(Resource):
    def post(self):
        try:
            lb_database = User.query.filter_by(username='lb').first()
        except:
            return {'response': 'Error reading database.'}, 403

        try:
            content = request.get_json()
            verify_password = User.verify_password(content["password"],
                                                   lb_database.password)
            username = content["username"].lower()
        except AttributeError:
            return {'response': 'Error: Must pass valid string.'}, 403
        if username != lb_database.username or verify_password is not \
                True:
            return {"message": "Bad username or password"}, 401
        access_token = create_access_token(identity=username)
        response = jsonify({"message": "login successful",
                            "token": access_token})
        set_access_cookies(response, access_token)

        return response


class logout(Resource):
    @jwt_required()
    def post(self):
        response = jsonify({"message": "logout successful"})
        unset_jwt_cookies(response)
        return response
##


class portainer_status(Resource):
    def get(self):
        global portainerstatus
        print(portainerstatus)
        return {'status': 200, 'running': portainerstatus}, 200


class portainer_start(Resource):
    @jwt_required()
    def get(self):
        global portainerstatus
        portainerstatus = True
        return {'status': 200, 'message': "success"}, 200


class portainer_stop(Resource):
    @jwt_required()
    def get(self):
        global portainerstatus
        portainerstatus = False

        time.sleep(10)

        return {'status': 200, 'message': "success"}, 200


class set_password(Resource):
    @jwt_required()
    def post(self):
        try:
            lb_database = User.query.filter_by(username='lb').first()
        except:
            return {'response': 'Error reading database.'}, 403

        try:
            content = request.get_json()
        except AttributeError:
            return {'response': 'Error: Must pass valid string.'}, 403

        try:
            hashed_password = User.hash_password(content["password"])
            lb_database.password = hashed_password
            lb_database.save_to_db()
            return {'response': 'done'}, 200
        except:
            return {'message': 'Something went wrong saving to'
                    'the database'}, 500


##
class settings_ui(Resource):
    def get(self):
        lb_database = User.query.filter_by(username='lb').first()
        return {'files': lb_database.files,
                'library': lb_database.library,
                'makerspace': lb_database.makerspace,
                'website': lb_database.website}, 200


class set_ui(Resource):
    @jwt_required()
    def post(self):
        try:
            lb_database = User.query.filter_by(username='lb').first()
        except:
            return {'response': 'Error reading database.'}, 403

        try:
            content = request.get_json()
        except AttributeError:
            return {'response': 'Error: Must pass valid string.'}, 403

        try:
            if "files" in content:
                if content["files"].lower() == "true":
                    lb_database.files = True
                elif content["files"].lower() == "false":
                    lb_database.files = False
            if "library" in content:
                if content["library"].lower() == "true":
                    lb_database.library = True
                elif content["library"].lower() == "false":
                    lb_database.library = False
            if "makerspace" in content:
                if content["makerspace"].lower() == "true":
                    lb_database.makerspace = True
                elif content["makerspace"].lower() == "false":
                    lb_database.makerspace = False
            if "website" in content:
                if content["website"].lower() == "true":
                    lb_database.website = True
                elif content["website"].lower() == "false":
                    lb_database.website = False

            lb_database.save_to_db()
            return {'response': 'done'}, 200
        except:
            return {'message': 'Something went wrong saving to '
                    'the database'}, 500


# /v1/update
class update(Resource):
    def get(self):

        return {'status': 202, 'message': "Accepted"}, 202


# /v1/uuid
class uuid(Resource):
    def get(self):

        return {'uuid': "asdsadsdf213qs2"}


class system_info(Resource):
    def get(self):
        return {"storage": {
                    'total': humansize(shutil.disk_usage("/tmp")[-0]),
                    'available': humansize(shutil.disk_usage("/tmp")[-1])
                    },
                "versions": {
                    "lb": VER
                    }
                }


class verify_login(Resource):
    def get(self):
        try:
            verify_jwt_in_request()
            return {'logged_in': True, 'user': get_jwt_identity()}, 200
        except Exception:
            return {'logged_in': False}, 401


# Network Endpoints
# /v1/wifi_connection_status
class wifi_connection_status(Resource):
    def get(self):
        global wifistatus
        return {'status': 200, 'running': wifistatus}, 200


# /v1/wifi_toggle
class wifi_toggle(Resource):
    def get(self):

        global wifistatus

        if wifistatus is False:
            print("WiFi is now up", flush=True)
            wifistatus = True

        elif wifistatus is True:
            print("WiFi is now down", flush=True)
            wifistatus = False

        return "This is a temporary path, not for production. " \
            f"Wifi is now set to {wifistatus}"


# /v1/wifi_forget
class wifi_forget(Resource):
    @jwt_required()
    def get(self):

        global wifistatus

        if wifistatus is False:
            return {
                'status': 409,
                'message': 'Device is already disconnected, connection '
                           'cannot be reset.'
            }, 409

        wifi_toggle().get()

        return {'status': 202, 'message': 'Reset request sent.'}, 202


# /v1/wifi_forget_all
class wifi_forget_all(Resource):
    @jwt_required()
    def get(self):

        global wifistatus

        if wifistatus is True:
            wifi_toggle().get()

        return {'status': 202, 'message': 'Reset request sent.'}, 202
