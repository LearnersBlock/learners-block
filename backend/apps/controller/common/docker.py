from dotenv import load_dotenv
from common.errors import print_message
import docker
import os

# Import .env file to make env vars available from os.environ
load_dotenv()

# Import relevant unix path
if os.environ['FLASK_ENV'].lower() == "production":
    client = docker.DockerClient(base_url='unix://var/run/balena-engine.sock')
else:
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')


class docker_py():
    def image_status(image):
        if client.images.list(image):
            return True
        else:
            return False

    def prune(image, network=None):
        try:
            client.images.remove(image=image)
        except docker.errors.ImageNotFound:
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

        return {"response": "done", "status_code": 200}

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
        except Exception as ex:
            print_message('docker.pull', 'Failed to pull container', ex)
            return {"response": str(ex), "status_code": 500}

        return {"response": str(response), "status_code": 200}

    def remove(name):
        try:
            container = client.containers.get(name)
            container.stop()
            container.remove()
        except Exception as ex:
            print_message('docker.remove', 'Failed to remove container', ex)
            return {"response": str(ex), "status_code": 500}

        return {"response": "done", "status_code": 200}

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
        except Exception as ex:
            print_message('docker.run', 'Failed to run container', ex)
            return {"response": str(ex), "status_code": 500}

        return {"response": str(response), "status_code": 200}

    def status(name):
        try:
            container = client.containers.get(name)
        except docker.errors.NotFound:
            return {"response": False, "status_code": 200}
        return {"response": str(container.status), "status_code": 200}
