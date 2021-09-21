from common.models import User
from common.system_processes import check_internet
from flask import request
from flask_jwt_extended import jwt_required
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


class set_wifi(Resource):
    @jwt_required()
    def post(self):
        global wifistatus
        content = request.get_json()
        lb_database = User.query.filter_by(username='lb').first()
        lb_database.wifi_password = content["wifi_password"]
        lb_database.save_to_db()
        return {'status': 200, 'running': wifistatus}, 200


class update(Resource):
    def get(self):
        return {'status': 202, 'message': "Accepted"}, 202


class uuid(Resource):
    def get(self):
        return {'uuid': "asdsadsdf213qs2"}


class wifi_connect(Resource):
    def post(self):
        content = request.get_json()

        return {'status': 202, 'message': content}, 202


class wifi_connection_status(Resource):
    def get(self):
        global wifistatus
        time.sleep(1.5)
        return {'status': 200, 'running': wifistatus,
                'connected': check_internet()}, 200


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


class wifi_list_access_points(Resource):
    @jwt_required()
    def get(self):
        # Demo routes
        return [{"ssid": "My House", "security": "WPA"},
                {"ssid": "TELUS9052-Enterprise", "security": "ENTERPRISE"},
                {"ssid": "Althaea-2-no-password", "security": "NONE"},
                {"ssid": "TELUS9052-Hidden", "security": "HIDDEN"}]
