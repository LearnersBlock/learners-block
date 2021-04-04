from dotenv import dotenv_values
from common.processes import check_internet
from common.processes import curl
from common.processes import human_size
from common.processes import rsync_get_status
from common.processes import rsync_terminate
from common.processes import rsync_download
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from werkzeug import serving
import shutil

# Import .version file
version = dotenv_values(".version")

# Import logging controller for log_request function
parent_log_request = serving.WSGIRequestHandler.log_request


# Function for disabling enpoint logging
def log_request(self, *args, **kwargs):
    if self.path == '/':
        return

    parent_log_request(self, *args, **kwargs)


class health_check(Resource):
    def get(self):

        serving.WSGIRequestHandler.log_request = log_request
        return {'status': 200, 'message': 'ok'}, 200


class hostname(Resource):
    def get(self):
        device_hostname = curl(method="get",
                               path="/v1/device/host-config?apikey=")
        return {
            'status': 200,
            'hostname': device_hostname["json_response"]
            ["network"]
            ["hostname"],
            'message': "OK"
        }, 200


class internet_connection_status(Resource):
    def get(self):
        if check_internet():
            return {'status': 200, 'connected': True}, 200
        else:
            return {'status': 206, 'connected': False}, 206


class rsync_fetch(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json()
            rsync_download(content["rsync_url"])
        except AttributeError:
            return {'response': 'Error: Must pass valid string.'}, 403

        return {'response': 'Process complete.'}, 200


class rsync_status(Resource):
    @jwt_required()
    def get(self):

        status = rsync_get_status()

        print(status, flush=True)

        # If out of space
        if status['progress'] == "space-error":
            return {'status': 200, 'progress': 1, "complete": True,
                    'speed': 0, 'transferred': 'Complete'}, 200

        # Send finished pattern when complete = true
        if status['complete'] is True:
            return {'status': 200, 'progress': 1, "complete": True,
                    'speed': 0, 'transferred': 'Complete'}, 200

        # Handle empty variables while the files are being checked
        if status['progress'][:-1] == '':
            return {'status': 200, 'progress': 'checking_files',
                    "complete": False,
                    'speed': 0, 'transferred': 0}, 200

        # Return current RSync progress
        return {'status': 200, 'progress': int(status['progress'][:-1])/100,
                'speed': status['speed'],
                'transferred': status['transferred'],
                'complete': False}, 200


class rsync_stop(Resource):
    def get(self):
        rsync_terminate()

        return {'status': 200, 'message': 'Terminate request sent'}, 200


class system_info(Resource):
    def get(self):
        return {"storage": {
                    'total': human_size(shutil.disk_usage("/tmp")[-0]),
                    'available': human_size(shutil.disk_usage("/tmp")[-1])
                },
                "versions": {
                    'lb': version["VERSION"]
                    }
                }
