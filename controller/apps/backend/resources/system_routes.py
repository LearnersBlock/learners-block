from common.docker import docker_py
from common.models import App_Store
from common.system_processes import check_internet
from common.system_processes import curl
from common.system_processes import human_size
from dotenv import dotenv_values
from flask_restful import Resource
from resources.errors import print_message
from werkzeug import serving
import json
import shutil

# Import .version file
version = dotenv_values(".version")

# Import logging controller for log_request function
parent_log_request = serving.WSGIRequestHandler.log_request


# Function for disabling logging on '/'
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


class system_info(Resource):
    def get(self):
        return {"storage": {
                    'total': human_size(shutil.disk_usage("/")[-0]),
                    'available': human_size(shutil.disk_usage("/")[-1])
                },
                "versions": {
                    'lb': version["VERSION"]
                    }
                }


class system_prune(Resource):
    def get(self):
        # Prune unused docker images
        installed_apps = App_Store.query.filter(App_Store.
                                                status == 'install')

        for app in installed_apps:
            # Prune dependencies
            try:
                if app.dependencies:
                    json_dep = json.loads(app.dependencies)
                    for dependency in json_dep:
                        deps = docker_py.prune(image=json_dep
                                               [dependency]
                                               ["image"],
                                               network=app.name)

                        print_message('app_store_set', deps["response"])
            except Exception as ex:
                print_message('app_store_set', deps["response"], ex)

            docker_py.prune(image=app.image, network=app.name)

        return {'status': 200, 'message': 'done'}, 200
