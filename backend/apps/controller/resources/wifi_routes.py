import config
import threading
from common.errors import logger
from common.models import User
from common.processes import check_connection
from common.processes import check_internet
from common.wifi import wifi
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class wifi_connect(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        wifi_connect_thread = threading.Thread(target=wifi.connect,
                                               kwargs=content)

        wifi_connect_thread.start()

        return {'message': 'Accepted'}


class wifi_connection_status(Resource):
    def get(self):
        return {'wifi': check_connection(),
                'internet': check_internet()}


class wifi_forget(Resource):
    @jwt_required()
    def get(self):
        # Check and store the current connection state
        connection_state = check_connection()

        # If the device is connected to a wifi network
        if not connection_state:
            return {
                'message': 'Device is already disconnected, '
                           'connection cannot be reset.'
            }, 409

        wifi_forget_thread = threading.Thread(target=wifi.forget,
                                              kwargs={'create_new_hotspot':
                                                      True,
                                                      'all_networks':
                                                      False})

        logger.info('Removing connetion...')

        wifi_forget_thread.start()

        return {'message': 'Accepted'}, 202


class wifi_forget_all(Resource):
    @jwt_required()
    def get(self):
        wifi_forget_thread_all = threading.Thread(
                                            target=wifi.forget_all,
                                            args=(1,),
                                            name='wifi_forget_thread_all')
        wifi_forget_thread_all.start()

        return {'message': 'Accepted'}, 202


class wifi_list_access_points(Resource):
    @jwt_required()
    def get(self):
        ssids, iw_status = wifi.list_access_points()

        return {'ssids': ssids, 'iw_compatible': iw_status}


class wifi_set_password(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        lb_database = User.query.filter_by(username=config.default_hostname
                                           ).first()
        lb_database.wifi_password = content["wifi_password"]
        lb_database.save_to_db()

        logger.debug(f'Wi-Fi password set to {content["wifi_password"]}')

        return {'message': 'success'}


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

        return {'message': 'success'}
