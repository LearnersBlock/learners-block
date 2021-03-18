from common.wifi import wifi
from flask_jwt_extended import jwt_required
from flask_restful import Resource
import threading


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
