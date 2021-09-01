from dotenv import load_dotenv
from resources.errors import print_message
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
    def prune(image, network):
        try:
            client.images.remove(image=image)
        except docker.errors.ImageNotFound:
            # If container was never installed then continue
            pass

        try:
            # Check that no dangling networks are left
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

    def run(env_vars, image, name, ports, volumes, network, detach=True):
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
                                             ports=ports,
                                             name=name,
                                             volumes=volumes,
                                             network=network,
                                             restart_policy={"Name": "always"})
        except Exception as ex:
            print_message('docker.run', 'Failed to run container', ex)
            return {"response": str(ex), "status_code": 500}

        return {"response": str(response), "status_code": 200}
