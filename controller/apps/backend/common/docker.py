from dotenv import load_dotenv
import docker
import os

# Import .env file to make env vars available from os.environ
load_dotenv()

# Import relevant unix path
if os.environ['FLASK_ENV'].lower() == "production":
    client = docker.DockerClient(base_url='unix://var/run/balena-engine.sock')
else:
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')


class docker():
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
            print(str(ex))
            return {"status_code": 500,
                    "response": str(ex)}

        return {"status_code": 200,
                "response": str(response)}

    def remove(name, image):
        try:
            container = client.containers.get(name)
            container.stop()
            container.remove()
            response = client.images.remove(image=image)
        except Exception as ex:
            print(str(ex))
            return {"status_code": 500,
                    "response": str(ex)}

        return {"status_code": 200,
                "response": str(response)}

    def run(image, name, ports, volumes, detach=True):
        try:
            response = client.containers.run(image,
                                             detach=True,
                                             ports=ports,
                                             name=name,
                                             volumes=volumes,
                                             restart_policy={"Name": "always"})
        except Exception as ex:
            print(str(ex))
            return {"status_code": 500,
                    "response": str(ex)}

        return {"status_code": 200,
                "response": str(response)}
