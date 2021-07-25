from common.database import update_container_db_status
from common.docker import docker
from common.processes import check_internet
from common.processes import curl
from common.processes import human_size
from dotenv import dotenv_values
from flask import request
from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
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


# Function for disabling enpoint logging
def log_request(self, *args, **kwargs):
    if self.path == '/':
        return

    parent_log_request(self, *args, **kwargs)


class docker_pull(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json()
        except AttributeError:
            return {'message': 'Error: Must pass valid string.'}, 403

        response = docker.pull(image=content["image"],
                               name=content["name"],
                               ports=content["ports"],
                               volumes=content["volumes"],
                               detach=True)

        update_container_db_status(content["name"], 'Installed')

        print(response["response"])

        return {"response": response["response"]}, response["status_code"]


class docker_remove(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json()
        except AttributeError:
            return {'message': 'Error: Must pass valid string.'}, 403

        response = docker.remove(name=content["name"],
                                 image=content["image"])

        update_container_db_status(content["name"], 'Install')

        if response["status_code"] == 200:
            print('docker_remove: container removed')
        else:
            print(response["response"])

        return {"response": response["response"]}, response["status_code"]


class docker_run(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json()
        except AttributeError:
            return {'message': 'Error: Must pass valid string.'}, 403

        response = docker.run(image=content["image"],
                              name=content["name"],
                              ports=content["ports"],
                              volumes=content["volumes"],
                              detach=True)

        update_container_db_status(content["name"], 'Installed')

        print(response["response"])

        return {"response": response["response"]}, response["status_code"]


class download_fetch(Resource):
    @jwt_required()
    def post(self):
        global download_log
        download_log = ''
        try:
            content = request.get_json()
        except AttributeError:
            return {'message': 'Error. Must pass valid string.'}, 403

        download_progress = threading.Thread(
                                target=download_fetch.download_file,
                                args=(self, content["download_url"]),
                                name='download_file')

        download_progress.start()

        def generate():
            global download_log
            global download_terminated
            download_terminated = 0
            while download_log is not True:
                if download_terminated == 1:
                    break
                if download_terminated != 0:
                    # An error occured
                    yield str(json.dumps({"error":
                                          download_terminated})) + "\n\n"
                    break
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
        except Exception:
            # Restore original UID
            os.seteuid(euid)
            download_stop.get(self, response='UID failure')
            return

        # Restore original UID
        os.seteuid(euid)

        try:
            try:
                total = int(resp.headers.get('content-length', 0))
            except Exception as ex:
                print(str(ex) + 'Setting file size to 0')
                total = 0

            with open(os.path.realpath('.') + '/storage/library/' +
                      url.split('/')[-1], 'wb') as file:

                global download_terminated
                downloaded_bytes = 0
                _, _, free = shutil.disk_usage("/tmp")
                for data in resp.iter_content(chunk_size=1024):
                    if download_terminated == 1:
                        break
                    size = file.write(data)
                    downloaded_bytes += size

                    # If running out of disk space exit
                    if downloaded_bytes + 100000000 > free:
                        download_stop.get(self, response='Out of disk space')
                        return
                    global download_log
                    download_log = json.dumps({
                        "progress": format(downloaded_bytes/total*100/100,
                                           ".4f"),
                        "mbytes": format(downloaded_bytes/1000000,
                                         ".4f"),
                    })
        except Exception as ex:
            print(str(ex))

        download_log = True
        print("Download complete")

        return {'message': 'process complete'}, 200


class download_stop(Resource):
    def get(self, response=1):
        # Terminate download upon user request
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
