import config
import json
import shutil
import time
from common.errors import logger
from common.docker import docker_py
from common.models import App_Store
from common.processes import container_hostname
from common.processes import database_recover
from common.processes import human_size
from dotenv import dotenv_values
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from werkzeug import serving

# Portainer version for LB system
portainer_image = "portainer/portainer-ce:2.6.3-alpine"

# Portainer volumes and CMD
volumes = [
    f"{config.socket_path}:{config.socket_path}",
    "portainer_data:/data",
]
command = f"-H unix:/{config.socket_path} " "-l portainer=hidden"

# Import .version file
version = dotenv_values(".version")

# Import logging controller for log_request function
parent_log_request = serving.WSGIRequestHandler.log_request


# Function for disabling logging on '/'
def log_request(self, *args, **kwargs):
    if self.path == "/":
        return

    parent_log_request(self, *args, **kwargs)


class system_health_check(Resource):
    def get(self):
        serving.WSGIRequestHandler.log_request = log_request
        return {"message": "ok"}


class system_hostname(Resource):
    def get(self):
        return {"hostname": container_hostname()}


class system_info(Resource):
    def get(self):
        return {
            "storage": {
                "total": human_size(shutil.disk_usage("/")[-0]),
                "available": human_size(shutil.disk_usage("/")[-1]),
            },
            "versions": {"lb": version["VERSION"]},
        }


class system_portainer(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # Portainer variables
        name = "portainer"
        ports = {"9000/tcp": 9000, "8000/tcp": 8000}
        privileged = True
        labels = {
            "io.balena.features.balena-socket": "1",
            "portainer": "hidden",
        }

        if content["cmd"] == "start":
            # Run the primary container
            container_status = docker_py.run(
                image=portainer_image,
                name=name,
                ports=ports,
                privileged=privileged,
                labels=labels,
                volumes=volumes,
                command=command,
            )

            logger.debug(f"Portainer status: {container_status}")

            return {"installed": container_status}

        elif content["cmd"] == "remove":
            # Remove the container (but not the image)
            container_status = docker_py.remove(name="portainer")

            logger.debug(f"Portainer status: {container_status}")

            return {"installed": container_status}

        elif content["cmd"] == "status":
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
        installed_apps = App_Store.query.filter(App_Store.status == "install")

        # Prune app store
        for app in installed_apps:
            # Prune app store dependencies
            try:
                if app.dependencies:
                    json_dep = json.loads(app.dependencies)
                    for dependency in json_dep:
                        docker_py.prune(
                            image=json_dep[dependency]["image"],
                            network=app.name,
                        )
            except Exception:
                logger.exception("Failed pruning app store dependencies.")

            docker_py.prune(image=app.image, network=app.name)

        # Prune Portainer image
        try:
            docker_py.prune(image=portainer_image)
        except Exception:
            logger.exception("Failed to remove Portainer image.")

        return {"message": "done"}


class system_reset_database(Resource):
    @jwt_required()
    def get(self):
        # Add delay as on occasion it does not process without it.
        time.sleep(1)
        database_recover()

        return {"message": "Forcing an error to activate polling."}, 410
