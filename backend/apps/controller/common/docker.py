import docker
import ntplib
import os
from common.errors import logger
from flask_restful import abort


# Import relevant UNIX path
if os.environ['FLASK_ENV'].lower() == "production":
    client_path = 'unix://var/run/balena-engine.sock'
else:
    client_path = 'unix://var/run/docker.sock'

# Initiate NTP Library
ntp = ntplib.NTPClient()


# Check time has been synced before request
def docker_ntp_check(func):
    def inner(*args, **kwargs):
        try:
            # Check if the system clock is in sync otherwise Docker Hub
            # certificates create an error
            time_offset = ntp.request('time.cloudflare.com', version=3).offset
            logger.info(f"Time offset is: {time_offset}")
            if time_offset > 3600 or time_offset < -3600:
                logger.debug('Not in sync with NTP server.')
                abort(502,
                      status=502,
                      message='System is still loading. Try again later.')
        except Exception:
            logger.exception('Failed to check time with NTP server.')
            # In event of connection error, allowing Docker to try anyway
            pass

        return func(*args, **kwargs)

    return inner


# Check Docker is available before sending the request
def docker_ping(func):
    def inner(*args, **kwargs):
        try:
            global client
            # If the Docker client is not yet initiated
            if 'client' not in globals():
                client = docker.DockerClient(base_url=client_path,
                                             tls=False)
            # Check the docker client is available
            client.ping()
        except Exception:
            logger.exception('Docker UNIX socket is unreachable.')
            abort(502,
                  status=502,
                  message='Docker service is unreachable.')

        return func(*args, **kwargs)

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
    @docker_ntp_check
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
    @docker_ntp_check
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
            # Returns here if the container does not exist
            return {"message": False, "status_code": 200}

        return {"message": str(container.status), "status_code": 200}
