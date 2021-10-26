from common.models import User
from common.processes import check_internet
from common.wifi import wifi
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
import config
import threading


class wifi_connect(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        if content["hiddenNetworkName"]:
            wifi.connect_to_AP(conn_type=content["hiddenSecurity"],
                               ssid=content["hiddenNetworkName"],
                               username=content["username"],
                               password=content["passphrase"])
        else:
            wifi.connect_to_AP(conn_type=content["type"],
                               ssid=content["ssid"],
                               username=content["username"],
                               password=content["passphrase"])

        return {'status': 200, 'message': 'Accepted'}, 200


class wifi_connection_status(Resource):
    def get(self):
        return {'status': 200,
                'wifi': wifi.check_connection(),
                'internet': check_internet()}, 200


class wifi_forget(Resource):
    @jwt_required()
    def get(self):
        # Check and store the current connection state
        connection_state = wifi.check_connection()

        # If the device is connected to a wifi network
        if not connection_state:
            return {
                'status': 409,
                'message': 'Device is already disconnected, '
                           'connection cannot be reset.'
            }, 409

        wifi_forget_thread = threading.Thread(target=wifi.forget,
                                              args=(config.ap_name,),
                                              name='wifi_forget_thread')
        wifi_forget_thread.start()

        return {'status': 202, 'message': 'Accepted'}, 202


class wifi_forget_all(Resource):
    @jwt_required()
    def get(self):
        wifi_forget_thread_all = threading.Thread(
                                            target=wifi.forget_all,
                                            args=(1,),
                                            name='wifi_forget_thread_all')
        wifi_forget_thread_all.start()

        return {'status': 202, 'message': 'Accepted'}, 202


class wifi_list_access_points(Resource):
    @jwt_required()
    def get(self):
        ssids, refresh_status = wifi.list_access_points()

        # Sort SSIDs by signal strength
        ssids = sorted(ssids,
                       key=lambda x: x['strength'],
                       reverse=True)

        return {'ssids': ssids, 'compatible': refresh_status}


class wifi_set_password(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        lb_database = User.query.filter_by(username=config.default_hostname
                                           ).first()
        lb_database.wifi_password = content["wifi_password"]
        lb_database.save_to_db()

        return {'message': 'success'}, 200


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

        return {'message': 'success'}, 200
