from dotenv import dotenv_values
from common.processes import curl, human_size
from flask_restful import Resource
from werkzeug import serving
import shutil

# Import .ver file
version = dotenv_values(".ver")

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
            'hostname': device_hostname,
            'message': "OK"
        }, 200


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
