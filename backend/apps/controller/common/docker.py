import config
import docker
from common.errors import DockerContainerException
from common.errors import DockerException
from common.errors import DockerImageStatus
from common.errors import DockerImageNotFound
from common.errors import DockerSocket
from common.errors import logger
from common.processes import container_hostname


# Check Docker is available before sending the request
def docker_ping(func):
    def inner(*args, **kwargs):
        try:
            global client
            # If the Docker client is not yet initiated.
            # Initiated here to avoid calling to early in boot sequence.
            if "client" not in globals():
                client = docker.DockerClient(
                    base_url=f"unix:/{config.socket_path}", tls=False
                )
            # Check the docker client is available
            client.ping()
        except Exception:
            logger.exception("Docker UNIX socket is unreachable.")
            raise DockerSocket

        return func(*args, **kwargs)

    return inner


class docker_py:
    @docker_ping
    def image_status(image):
        try:
            if client.images.list(image):
                return True
            else:
                return False
        except docker.errors.APIError:
            logger.exception("Failed getting image status.")
            raise DockerImageStatus

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

        return True

    @docker_ping
    def pull(env_vars, image, name, ports, volumes, network, detach=True):
        try:
            container = client.containers.get(name)
            client.images.pull(image)
            container.stop()
            container.remove()

            # Run the pulled containers
            response = docker_py.run(
                env_vars=env_vars,
                image=image,
                detach=True,
                name=name,
                ports=ports,
                volumes=volumes,
                network=network,
            )
        except docker.errors.NotFound:
            logger.exception("Docker image not found.")
            raise DockerImageNotFound
        except Exception:
            logger.exception("Failed to pull container.")
            raise DockerException

        return str(response)

    @docker_ping
    def remove(name):
        try:
            container = client.containers.get(name)
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            logger.exception("Docker image not found. Continuing.")
        except Exception:
            logger.exception("Failed to remove container.")
            raise DockerException

        return True

    @docker_ping
    def run(
        image,
        name,
        ports={},
        volumes={},
        detach=True,
        network="lbsystem",
        env_vars={},
        privileged=False,
        command="",
        labels={},
    ):
        # If network doesn't yet exist then create it
        try:
            client.networks.create(
                network, driver="bridge", check_duplicate=True
            )
        except docker.errors.APIError:
            # Network already exists
            pass

        # Add default env vars for all containers
        evars = {"DEVICE_HOSTNAME": container_hostname()}
        env_vars.update(evars)

        try:
            response = client.containers.run(
                image,
                environment=env_vars,
                detach=True,
                privileged=privileged,
                ports=ports,
                name=name,
                labels=labels,
                volumes=volumes,
                network=network,
                restart_policy={"Name": "always"},
                command=command,
            )
        except docker.errors.NotFound:
            logger.exception("Docker image not found.")
            raise DockerImageNotFound
        except docker.errors.ContainerError:
            logger.exception("Container exited with non-zero code.")
            raise DockerContainerException
        except docker.errors.ImageNotFound:
            logger.exception("Docker image not found.")
            raise DockerImageNotFound
        except Exception:
            logger.exception("Failed to run container. Unknown error.")
            raise DockerException

        return str(response)

    @docker_ping
    def status(name):
        try:
            container = client.containers.get(name)
        except docker.errors.NotFound:
            # Returns here if the container does not exist
            return False

        return str(container.status)
