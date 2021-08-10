from common.database import update_container_db_status
from common.docker import docker_py
from common.models import App_Store
from common.processes import check_internet
from common.processes import curl
from common.processes import human_size
from dotenv import dotenv_values
from flask import request
from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from resources.errors import print_message
from werkzeug import serving
import json
import shutil
import time
import threading
import os
import requests

# Import .version file
version = dotenv_values(".version")

# Import logging controller for log_request function
parent_log_request = serving.WSGIRequestHandler.log_request


# Function for disabling logging on '/'
def log_request(self, *args, **kwargs):
    if self.path == '/':
        return

    parent_log_request(self, *args, **kwargs)


class docker_pull(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # If there are container dependencies, pull those too
        if content["dependencies"]:
            for dependency in content["dependencies"]:
                deps = docker_py.pull(env_vars=content["dependencies"]
                                      [dependency]["env_vars"],
                                      image=content["dependencies"]
                                      [dependency]["image"],
                                      name=dependency,
                                      ports=content["dependencies"]
                                      [dependency]["ports"],
                                      volumes=content["dependencies"]
                                      [dependency]["volumes"],
                                      network=content["name"],
                                      detach=True)

                print_message('docker_pull', deps["response"])

        # Pull latest containers and run them
        response = docker_py.pull(env_vars=content["env_vars"],
                                  image=content["image"],
                                  name=content["name"],
                                  ports=content["ports"],
                                  volumes=content["volumes"],
                                  network=content["name"],
                                  detach=True)

        # Update the database with new container state
        update_container_db_status(content["name"], 'installed')

        return {"response": response["response"]}, response["status_code"]


class docker_remove(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # If there are container dependencies then remove them
        if content["dependencies"]:
            for dependency in content["dependencies"]:
                deps = docker_py.remove(name=dependency)

                print_message('docker_remove', deps["response"])

        # Remove main container
        response = docker_py.remove(name=content["name"])

        # Update the database with new container state
        update_container_db_status(content["name"], 'install')

        return {"response": response["response"]}, response["status_code"]


class docker_run(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # If there are container dependencies start them
        if content["dependencies"]:
            for dependency in content["dependencies"]:
                deps = docker_py.run(env_vars=content["dependencies"]
                                     [dependency]["env_vars"],
                                     image=content["dependencies"]
                                     [dependency]["image"],
                                     name=dependency,
                                     ports=content["dependencies"]
                                     [dependency]["ports"],
                                     volumes=content["dependencies"]
                                     [dependency]["volumes"],
                                     network=content["name"],
                                     detach=True)

                print_message('docker_run', deps["response"])

        # Run the primary container
        response = docker_py.run(env_vars=content["env_vars"],
                                 image=content["image"],
                                 name=content["name"],
                                 ports=content["ports"],
                                 volumes=content["volumes"],
                                 network=content["name"],
                                 detach=True)

        # Update the database with new container state
        update_container_db_status(content["name"], 'installed')

        return {"response": response["response"]}, response["status_code"]


class download_fetch(Resource):
    @jwt_required()
    def post(self):
        # Set vars
        global download_log
        download_log = ''
        content = request.get_json()

        # Fetch the requested file
        download_progress = threading.Thread(
                                target=download_fetch.download_file,
                                args=(self, content["download_url"]),
                                name='download_file')

        download_progress.start()

        # Stream the download progress via the api
        def generate():
            # Set vars
            global download_log
            global download_terminated
            download_terminated = 0
            # While the download is running loop
            while download_log is not True:
                # If download is complete or terminate command is sent
                # via download_stop
                if download_terminated == 1:
                    break
                # If download_terminated is not 1 or 0 then report error
                if download_terminated != 0:
                    # An error occured
                    yield str(json.dumps({"error":
                                          download_terminated})) + "\n\n"
                    break
                # Stream last line
                yield str(download_log) + "\n\n"
                time.sleep(2)

        return Response(generate(), mimetype="text/event-stream")

    def download_file(self, url):
        # Store current UID
        euid = os.geteuid()

        try:
            # Set UID for this download
            if os.environ['FLASK_ENV'].lower() == "production":
                os.seteuid(65534)
            resp = requests.get(url, stream=True, timeout=5)
        except Exception as ex:
            print_message('download_file', 'Failed setting euid', ex)
            # Restore original UID
            os.seteuid(euid)
            download_stop.get(self, response='UID failure')
            return

        # Restore original UID
        os.seteuid(euid)

        # Get length of file for progress reporting
        try:
            total = int(resp.headers.get('content-length', 0))
        except Exception as ex:
            # If cannot get file length, set to 0 to avoid errors
            print_message('donwload_files',
                          'failed getting content-length', ex)
            total = 0

        # Set the download path
        with open(os.path.realpath('.') + '/storage/library/' +
                  url.split('/')[-1], 'wb') as file:

            # Set vars
            global download_terminated
            downloaded_bytes = 0

            # Get free disk space
            _, _, free = shutil.disk_usage("/tmp")

            # For each chunk write to file to avoid memory overload
            for data in resp.iter_content(chunk_size=1024):
                # If a stop request has been sent
                if download_terminated == 1:
                    break
                size = file.write(data)
                downloaded_bytes += size

                # If running out of disk space exit
                if downloaded_bytes + 100000000 > free:
                    download_stop.get(self, response='Out of disk space')
                    return

                # Format and create response for streaming via download_fetch
                global download_log
                download_log = json.dumps({
                    "progress": format(downloaded_bytes/total*100/100,
                                       ".4f"),
                    "mbytes": format(downloaded_bytes/1000000,
                                     ".4f"),
                })

        # Reset global var for next use
        download_log = True

        return {'message': 'process complete'}, 200


class download_stop(Resource):
    def get(self, response=1):
        # Terminate by setting global var for reading in other functions
        global download_terminated
        download_terminated = response

        return {'status': 200, 'message': 'terminate request sent'}, 200


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
                    'total': human_size(shutil.disk_usage("/tmp")[-0]),
                    'available': human_size(shutil.disk_usage("/tmp")[-1])
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
