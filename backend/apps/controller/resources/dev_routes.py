import config
import time
from common.errors import logger
from common.models import User
from common.processes import check_internet
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


# Set default Wi-Fi status for mock endpoint
wifistatus = True
portainerstatus = False


def wifi_toggle():
    global wifistatus

    if wifistatus is False:
        logger.info("WiFi is now up")
        wifistatus = True

    elif wifistatus is True:
        logger.info("WiFi is now down")
        wifistatus = False

    return "This is a dev function, not for production. " \
        f"Wifi is now set to {wifistatus}"


class supervisor_device(Resource):
    def get(self):
        return {'message': 'output'}


class supervisor_host_config(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # Trim whitespace at begining and end of string
        content["hostname"] = content["hostname"].strip()

        time.sleep(2)
        logger.info(f"Hostname changed to '{content['hostname']}'")
        return {
            'message': "Hostname/Wi-Fi SSID changed"
            f"to '{content['hostname']}'"
        }


class supervisor_journal_logs(Resource):
    def get(self):
        return "journal logs..."


class supervisor_state(Resource):
    def get(self):
        supervisor_state = True

        # Demo response
        response = {
            "status": "success",
            "containers": [
                {
                    "status": "Running",
                    "serviceName": "controller",
                    "appId": 1854775,
                    "imageId": 4192930,
                    "serviceId": 1178950,
                    "containerId": "c4402e5f5ee5e...",
                    "createdAt": "2021-10-31T18:02:41.272Z"
                    },
                {
                    "status": "Running",
                    "serviceName": "frontend",
                    "appId": 1854775,
                    "imageId": 4192931,
                    "serviceId": 1178951,
                    "containerId": "473a71f3ec2745...",
                    "createdAt": "2021-10-31T17:50:18.377Z"
                }
            ],
            "release": "aaf4aad197d58e52f5edd0cbbdaad814"
            }

        for key in response['containers']:
            if key['status'].lower() != 'running':
                logger.warning("Supervisor reports container "
                               f"'{key['serviceName']}' is not in state "
                               "'Running'.")
                supervisor_state = False

        return {'message': supervisor_state}


class supervisor_update(Resource):
    def get(self):
        return {'message': "Accepted"}, 202


class supervisor_uuid(Resource):
    def get(self):
        return {'uuid': "asdsadsdf213qs2"}


class wifi_connect(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        return {'message': content}, 202


class wifi_connection_status(Resource):
    def get(self):
        global wifistatus
        time.sleep(1.5)
        return {'wifi': wifistatus, 'internet': check_internet()}


class wifi_forget(Resource):
    @jwt_required()
    def get(self):
        global wifistatus

        if wifistatus is False:
            return {
                'message': 'Device is already disconnected, connection '
                           'cannot be reset.'
            }, 409

        wifi_toggle()

        return {'message': 'Accepted'}, 202


class wifi_forget_all(Resource):
    @jwt_required()
    def get(self):
        global wifistatus

        if wifistatus is True:
            wifi_toggle()

        return {'message': 'Accepted'}, 202


class wifi_list_access_points(Resource):
    @jwt_required()
    def get(self):
        time.sleep(2)
        # Demo routes
        ssids = [{"ssid": "My House", "security": "WPA",
                  "strength": 70},
                 {"ssid": "TELUS9052-Enterprise",
                  "security": "ENTERPRISE",
                  "strength": 100},
                 {"ssid": "Althaea-2-no-password",
                  "security": "NONE",
                  "strength": 1},
                 {"ssid": "TELUS9052-Hidden", "security": "HIDDEN",
                  "strength": 10}]

        # Sort SSIDs by signal strength
        ssids = sorted(ssids,
                       key=lambda x: x['strength'],
                       reverse=True)

        return {'ssids': ssids, 'compatible': True}


class wifi_set_password(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        lb_database = User.query.filter_by(username=config.default_hostname
                                           ).first()
        lb_database.wifi_password = content["wifi_password"]
        lb_database.save_to_db()

        return {'running': 'success'}


class wifi_set_ssid(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # Trim whitespace at begining and end of string
        content["ssid"] = content["ssid"].strip()

        if content["ssid"] == config.default_hostname:
            content["ssid"] = config.default_ssid

        lb_database = User.query.filter_by(username=config.default_hostname
                                           ).first()
        lb_database.wifi_ssid = content["ssid"]
        lb_database.save_to_db()

        logger.info(f"Wi-Fi SSID changed to '{content['ssid']}'")

        return {'running': 'success'}
