import config
import json
import shutil
import time
from common.errors import logger
from common.docker import docker_py
from common.models import App_Store
from common.processes import curl
from common.processes import database_recover
from common.processes import human_size
from dotenv import dotenv_values
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from werkzeug import serving

# Portainer version for LB system
portainer_image = "portainer/portainer-ce:2.6.3-alpine"

# Import .version file
version = dotenv_values(".version")

# Import logging controller for log_request function
parent_log_request = serving.WSGIRequestHandler.log_request


# Function for disabling logging on '/'
def log_request(self, *args, **kwargs):
    if self.path == '/':
        return

    parent_log_request(self, *args, **kwargs)


class system_health_check(Resource):
    def get(self):
        serving.WSGIRequestHandler.log_request = log_request
        return {'status': 200, 'message': 'ok'}


class system_hostname(Resource):
    def get(self):
        device_hostname = curl(method="get",
                               path="/v1/device/host-config?apikey=")

        logger.debug(f'System hostname status: {device_hostname}')

        return {
            'status': 200,
            'hostname': device_hostname["json_response"]
                                       ["network"]
                                       ["hostname"],
            'message': "OK"
        }


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


class system_portainer(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # Portainer variables
        name = "portainer"
        ports = {"9000/tcp": 9000, "8000/tcp": 8000}
        privileged = True
        labels = {"io.balena.features.balena-socket": "1",
                  "portainer": "hidden"}

        # Connect to standard docker if in dev env
        if config.dev_mode:
            volumes = ['/var/run/docker.sock:/var/run/docker.sock',
                       'portainer_data:/data']
            command = "-H unix://var/run/docker.sock " \
                      "-l portainer=hidden"
        else:
            volumes = \
                ['/var/run/balena-engine.sock:/var/run/balena-engine.sock',
                 'portainer_data:/data']
            command = "-H unix://var/run/balena-engine.sock " \
                      "-l portainer=hidden"

        if content['cmd'] == 'start':
            # Run the primary container
            container_status = docker_py.run(image=portainer_image,
                                             name=name,
                                             ports=ports,
                                             privileged=privileged,
                                             labels=labels,
                                             volumes=volumes,
                                             command=command)

            logger.debug(f'Portainer status: {container_status}')

            return {"installed": container_status}

        elif content['cmd'] == 'remove':
            # Remove the container (but not the image)
            container_status = docker_py.remove(name="portainer")

            logger.debug(f'Portainer status: {container_status}')

            return {"installed": container_status}

        elif content['cmd'] == 'status':
            # Fetch container status and check if image exists on the system
            container_status = docker_py.status(name="portainer")

            if container_status is not False:
                return {"installed": container_status}
            else:
                image_status = docker_py.image_status(portainer_image)
                return {"installed": False, "image": image_status}


class system_prune(Resource):
    @jwt_required()
    def get(self):
        installed_apps = App_Store.query.filter(App_Store.
                                                status == 'install')

        # Prune app store
        for app in installed_apps:
            # Prune app store dependencies
            try:
                if app.dependencies:
                    json_dep = json.loads(app.dependencies)
                    for dependency in json_dep:
                        docker_py.prune(image=json_dep
                                        [dependency]
                                        ["image"],
                                        network=app.name)
            except Exception:
                logger.exception('Failed pruning app store dependencies.')

            docker_py.prune(image=app.image, network=app.name)

        # Prune Portainer image
        try:
            docker_py.prune(image=portainer_image)
        except Exception:
            logger.exception("Failed to remove Portainer image.")

        return {'status': 200, 'message': 'done'}


class system_reset_database(Resource):
    @jwt_required()
    def get(self):
        # Add delay to ensure request is processed.
        time.sleep(5)
        database_recover()

        return {'message': 'Forcing an error to activate polling.'}, 410
