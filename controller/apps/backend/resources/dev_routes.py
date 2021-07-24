from flask_jwt_extended import jwt_required
from flask import request
from flask_restful import Resource
import subprocess
import time


# Set default Wi-Fi status for mock endpoint
wifistatus = True
portainerstatus = False


def wifi_toggle():

    global wifistatus

    if wifistatus is False:
        print("WiFi is now up")
        wifistatus = True

    elif wifistatus is True:
        print("WiFi is now down")
        wifistatus = False

    return "This is a dev function, not for production. " \
        f"Wifi is now set to {wifistatus}"


class device(Resource):
    def get(self):
        return {'message': 'output'}, 200


class host_config(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        print(f"Hostname changed to '{content['hostname']}'")
        return {
            'status': 200,
            'message': f"Hostname changed to '{content['hostname']}'"
        }, 200


class hostname(Resource):
    def get(self):
        container_hostname = subprocess.run(["hostname"], capture_output=True,
                                            text=True).stdout.rstrip()
        return {
            'status': 200,
            'hostname': container_hostname,
            'message': "OK"
        }, 200


class journal_logs(Resource):
    def get(self):

        return "journal logs..."


class portainer_status(Resource):
    def get(self):
        global portainerstatus
        time.sleep(5)
        if portainerstatus is True:
            return {'status': 200, 'container_status': 'Running'}, 200
        else:
            return {'status': 200, 'container_status': 'Stopped'}, 200


class portainer_start(Resource):
    @jwt_required()
    def get(self):
        global portainerstatus
        time.sleep(3)
        portainerstatus = True
        return {'status': 200,
                'message': "Supervisor responses here"}, 200


class portainer_stop(Resource):
    @jwt_required()
    def get(self):
        global portainerstatus
        time.sleep(3)
        portainerstatus = False

        return {'status': 200,
                'message': "Supervisor responses here"}, 200


class update(Resource):
    def get(self):

        return {'status': 202, 'message': "Accepted"}, 202


class uuid(Resource):
    def get(self):

        return {'uuid': "asdsadsdf213qs2"}


class wifi_connection_status(Resource):
    def get(self):
        global wifistatus
        time.sleep(3)
        return {'status': 200, 'running': wifistatus}, 200


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

        wifi_toggle()

        return {'status': 202, 'message': 'Accepted'}, 202


class wifi_forget_all(Resource):
    @jwt_required()
    def get(self):

        global wifistatus

        if wifistatus is True:
            wifi_toggle()

        return {'status': 202, 'message': 'Accepted'}, 202
