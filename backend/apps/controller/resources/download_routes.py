import json
import os
import requests
import shutil
import threading
import time
from common.errors import logger
from common.processes import chronyd_check
from flask import request
from flask import Response
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class download_fetch(Resource):
    @jwt_required()
    @chronyd_check
    def post(self):
        # Set vars
        global download_log
        global download_terminated
        download_terminated = 0
        download_log = ""
        content = request.get_json()

        # Fetch the requested file
        download_progress = threading.Thread(
            target=download_fetch.download_file,
            args=(self, content["download_url"]),
            name="download_file",
        )

        download_progress.start()

        return {"message": "process started"}

    def download_file(self, url):
        try:
            resp = requests.get(url, stream=True, timeout=5)
            resp.raise_for_status()
        except Exception:
            # As this runs in a thread, no use aborting or raising error
            logger.exception("Failed downloading file.")
            download_stop.get(self, response="failed download")
            return

        # Get length of file for progress reporting
        try:
            total = int(resp.headers.get("content-length", 0))
        except Exception:
            # If cannot get file length, set to 0 to avoid errors
            # As this runs in a thread, no use aborting or raising error
            logger.exception("Failed getting content-length.")
            total = 0

        # Set the download path
        filePath = (
            os.path.realpath(".") + "/storage/library/" + url.split("/")[-1]
        )

        with open(filePath, "wb") as file:
            # Set vars
            global download_terminated
            downloaded_bytes = 0

            # Get free disk space
            _, _, free = shutil.disk_usage("/")

            # For each chunk write to file to avoid memory overload
            for data in resp.iter_content(chunk_size=1024):
                # If a stop request has been sent
                if download_terminated == 1:
                    try:
                        os.remove(filePath)
                    except Exception:
                        # If none of the was downloaded then continue
                        pass
                    break
                size = file.write(data)
                downloaded_bytes += size

                # If running out of disk space exit
                if downloaded_bytes + 100000000 > free:
                    download_stop.get(self, response="Out of disk space")
                    return

                # Format and create response for streaming via download_fetch
                global download_log
                download_log = json.dumps(
                    {
                        "progress": int(float(downloaded_bytes / total * 100)),
                        "mbytes": int(float(downloaded_bytes / 1000000)),
                    }
                )

        # Set file permission for access via NGINX and PHP
        if os.path.isfile(filePath):
            os.chown(filePath, 65534, 65534)

        # Reset global var for next use
        download_log = True

        return {"message": "process complete"}


class download_stop(Resource):
    def get(self, response=1):
        # Terminate by setting global var for reading in other functions
        global download_terminated
        download_terminated = response

        return {"message": "terminate request sent"}


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
                    yield str(
                        json.dumps({"error": download_terminated})
                    ) + "\n\n"
                    break
                # Stream last line
                yield str(download_log) + "\n\n"
                time.sleep(2)

        return Response(generate(), mimetype="text/event-stream")
