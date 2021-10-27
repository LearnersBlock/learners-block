import docker
import os
from common.errors import logger
from flask_restful import abort

try:
    # Import relevant UNIX path
    if os.environ['FLASK_ENV'].lower() == "production":
        client = \
            docker.DockerClient(base_url='unix://var/run/balena-engine.sock')
    else:
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
except Exception:
    logger.error('Docker socket is unavailable.')
    pass


# Check Docker is available before sending the request
def docker_ping(func):
    def inner(*args, **kwargs):
        try:
            client.ping()
            return func(*args, **kwargs)
        except docker.errors.APIError:
            logger.exception('Docker UNIX socket is unreachable.')
            abort(502,
                  status=502,
                  message='Docker service is unreachable.',)
    return inner


class docker_py():
    @docker_ping
    def image_status(image):
        try:
            if client.images.list(image):
                return True
            else:
                return False
        except docker.errors.APIError:
            logger.exception('Failed getting image status.')

    @docker_ping
    def prune(image, network=None):
        try:
            client.images.remove(image=image)
        except Exception:
            # If image was never downloaded then continue
            pass

        try:
            # Check that no dangling networks are left
            if network is not None:
                app_network = client.networks.get(network)
                app_network.remove()
        except Exception:
            # Pass if network had already been removed
            pass

        return {"message": "done", "status_code": 200}

    @docker_ping
    def pull(env_vars, image, name, ports, volumes, network, detach=True):
        try:
            container = client.containers.get(name)
            client.images.pull(image)
            container.stop()
            container.remove()

            # Run the pulled containers
            response = docker_py.run(env_vars=env_vars,
                                     image=image,
                                     detach=True,
                                     name=name,
                                     ports=ports,
                                     volumes=volumes,
                                     network=network)
        except docker.errors.NotFound as ex:
            logger.exception("Docker image not found.")
            return {"message": str(ex), "status_code": 500}
        except Exception as ex:
            logger.exception("Failed to pull container.")
            return {"message": str(ex), "status_code": 500}

        return {"message": str(response), "status_code": 200}

    @docker_ping
    def remove(name):
        try:
            container = client.containers.get(name)
            container.stop()
            container.remove()
        except docker.errors.NotFound as ex:
            logger.exception("Docker image not found.")
            return {"message": str(ex), "status_code": 500}
        except Exception as ex:
            logger.exception("Failed to remove container.")
            return {"message": str(ex), "status_code": 500}

        return {"message": "done", "status_code": 200}

    @docker_ping
    def run(image, name, ports={}, volumes={}, detach=True, network='lbsystem',
            env_vars={}, privileged=False, command='', labels={}):
        # If network doesn't yet exist, create it
        try:
            client.networks.create(network,
                                   driver="bridge",
                                   check_duplicate=True)
        except docker.errors.APIError:
            # Network already exists
            pass

        try:
            response = client.containers.run(image,
                                             environment=env_vars,
                                             detach=True,
                                             privileged=privileged,
                                             ports=ports,
                                             name=name,
                                             labels=labels,
                                             volumes=volumes,
                                             network=network,
                                             restart_policy={"Name": "always"},
                                             command=command)
        except docker.errors.ContainerError as ex:
            logger.exception("Container exited with non-zero code.")
            return {"message": str(ex), "status_code": 500}
        except docker.errors.ImageNotFound as ex:
            logger.exception("Docker image not found.")
            return {"message": str(ex), "status_code": 500}
        except Exception as ex:
            logger.exception("Failed to run container.")
            return {"message": str(ex), "status_code": 500}

        return {"message": str(response), "status_code": 200}

    @docker_ping
    def status(name):
        try:
            container = client.containers.get(name)
        except docker.errors.NotFound:
            return {"message": False, "status_code": 200}
        return {"message": str(container.status), "status_code": 200}
