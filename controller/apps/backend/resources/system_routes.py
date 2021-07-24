from dotenv import dotenv_values
from common.docker import docker
from common.database import update_container_db_status
from common.downloads import download_get_status
from common.downloads import download_start
from common.downloads import download_terminate
from common.downloads import rsync_get_status
from common.downloads import rsync_start
from common.downloads import rsync_terminate
from common.processes import check_internet
from common.processes import curl
from common.processes import human_size
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


class docker_pull(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json()
        except AttributeError:
            return {'message': 'Error: Must pass valid string.'}, 403

        response = docker.pull(image=content["image"],
                               name=content["name"],
                               ports=content["ports"],
                               volumes=content["volumes"],
                               detach=True)

        update_container_db_status(content["name"], 'Installed')

        print(response["response"])

        return {"response": response["response"]}, response["status_code"]


class docker_remove(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json()
        except AttributeError:
            return {'message': 'Error: Must pass valid string.'}, 403

        response = docker.remove(name=content["name"],
                                 image=content["image"])

        update_container_db_status(content["name"], 'Install')

        if response["status_code"] == 200:
            print('docker_remove: container removed')
        else:
            print(response["response"])

        return {"response": response["response"]}, response["status_code"]


class docker_run(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json()
        except AttributeError:
            return {'message': 'Error: Must pass valid string.'}, 403

        response = docker.run(image=content["image"],
                              name=content["name"],
                              ports=content["ports"],
                              volumes=content["volumes"],
                              detach=True)

        update_container_db_status(content["name"], 'Installed')

        print(response["response"])

        return {"response": response["response"]}, response["status_code"]


class download_fetch(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json()
        except AttributeError:
            return {'message': 'Error: Must pass valid string.'}, 403

        download_start(content["download_url"])

        return {'message': 'process complete'}, 200


class download_status(Resource):
    def get(self):
        status = download_get_status()

        print(status)

        # Return current download progress
        return status, 200


class download_stop(Resource):
    def get(self):
        download_terminate()

        return {'status': 200, 'message': 'terminate request sent'}, 200


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
        except AttributeError:
            return {'message': 'Error: Must pass valid string.'}, 403

        rsync_start(content["rsync_url"])

        return {'message': 'process complete'}, 200


class rsync_status(Resource):
    def get(self):

        status = rsync_get_status()

        print(status)

        return status


class rsync_stop(Resource):
    def get(self):
        rsync_terminate()

        return {'status': 200, 'message': 'terminate request sent'}, 200


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
