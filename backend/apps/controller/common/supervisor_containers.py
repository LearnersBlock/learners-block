from common.system_processes import curl
from flask_restful import abort
import os
import time


class container:
    def start(container_name, sleep=0):
        time.sleep(sleep)
        response = curl(method="post-data",
                        path=f"/v2/applications/{os.environ['BALENA_APP_ID']}"
                               "/start-service?apikey=",
                        string='{"serviceName": "%s"}' % (container_name))

        return response

    def status(container_name):
        # Get running containers
        response = curl(method="get",
                        path="/v2/state/status?apikey=")

        # Find the container required and return status
        for entry in response["json_response"]["containers"]:
            if entry['serviceName'] == container_name:
                return response, entry

        # If container isn't found, abort with error
        abort(404, status=404,
              message='Container not found')

    def stop(container_name, sleep=0):
        time.sleep(sleep)
        response = curl(method="post-data",
                        path=f"/v2/applications/{os.environ['BALENA_APP_ID']}"
                               "/stop-service?apikey=",
                        string='{"serviceName": "%s"}' % (container_name))

        return response
