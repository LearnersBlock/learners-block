from flask import request
from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from resources.errors import print_message
import json
import shutil
import time
import threading
import os
import requests


class download_fetch(Resource):
    @jwt_required()
    def post(self):
        # Set vars
        global download_log
        global download_terminated
        download_terminated = 0
        download_log = ''
        content = request.get_json()

        # Fetch the requested file
        download_progress = threading.Thread(
                                target=download_fetch.download_file,
                                args=(self, content["download_url"]),
                                name='download_file')

        download_progress.start()

        return {'message': 'process started'}

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
            _, _, free = shutil.disk_usage("/")

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
                    "progress": int(float(downloaded_bytes/total*100)),
                    "mbytes": int(float(downloaded_bytes/1000000)),
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


class download_stream(Resource):
    def get(self):
        # Stream the download progress via the api
        def generate():
            # Set vars
            global download_log
            global download_terminated
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
