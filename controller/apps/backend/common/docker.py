from dotenv import load_dotenv
from resources.errors import print_error
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
    def pull(image, name, ports, volumes, detach=True):
        try:
            container = client.containers.get(name)
            client.images.pull(image)
            container.stop()
            container.remove()
            response = docker.run(image=image,
                                  detach=True,
                                  name=name,
                                  ports=ports,
                                  volumes=volumes)
        except Exception as ex:
            print_error('docker.pull', 'Failed to pull container', ex)
            return {"response": str(ex), "status_code": 500}

        return {"response": str(response), "status_code": 200}

    def prune(image):
        try:
            client.images.remove(image=image)
        except docker.errors.ImageNotFound:
            # If container was never installed then continue
            pass

        return {"response": "done", "status_code": 200}

    def remove(name, image):
        try:
            container = client.containers.get(name)
            container.stop()
            container.remove()
        except Exception as ex:
            print_error('docker.remove', 'Failed to remove container', ex)
            return {"response": str(ex), "status_code": 500}

        return {"response": "done", "status_code": 200}

    def run(image, name, ports, volumes, detach=True):
        try:
            response = client.containers.run(image,
                                             detach=True,
                                             ports=ports,
                                             name=name,
                                             volumes=volumes,
                                             restart_policy={"Name": "always"})
        except Exception as ex:
            print_error('docker.run', 'Failed to run container', ex)
            return {"response": str(ex), "status_code": 500}

        return {"response": str(response), "status_code": 200}
