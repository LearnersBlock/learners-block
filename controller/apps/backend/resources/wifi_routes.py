from common.models import User
from common.wifi import wifi
from common.wifi import wifi_connect
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import abort
from flask_restful import Resource
from resources.errors import print_message
import threading


class set_wifi(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        lb_database = User.query.filter_by(username='lb').first()
        lb_database.wifi_password = content["wifi_password"]
        lb_database.save_to_db()

        # If connected, restart Wi-Fi-Connect
        connected = wifi().check_connection()
        if not connected:
            try:
                wifi_connect().stop()
                wifi_connect().start(wait=2)
            except Exception as ex:
                print_message('set_wifi',
                              'Failed starting wifi-connect',
                              ex)
                abort(500, status=500,
                      message='Wifi-connect failed to launch',
                      error=str(ex))

        return {'message': 'success'}, 200


class wifi_connection_status(Resource):
    def get(self):
        response = wifi().check_connection()

        if response:
            return {'status': 200, 'running': True}, 200
        else:
            return {'status': 206, 'running': False}, 206


class wifi_forget(Resource):
    @jwt_required()
    def get(self):
        # Check and store the current connection state
        connection_state = wifi().check_connection()

        # If the device is connected to a wifi network
        if not connection_state:
            return {
                'status': 409,
                'message': 'Device is already disconnected, '
                           'connection cannot be reset.'
            }, 409

        wifi_forget_thread = threading.Thread(target=wifi.forget,
                                              args=(1,),
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
