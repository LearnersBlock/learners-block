from flask_restful import abort
from common.processes import curl
import inspect
import os
import time


class container:
    def status(self, container_name, sleep=0):
        time.sleep(sleep)
        response = curl(method="get",
                        path="/v2/state/status?apikey=")

        for entry in response["json_response"]["containers"]:
            if entry['serviceName'] == container_name:
                return response, entry

        abort(404, status=404,
              message='Container not found')

    def start(self, container_name, sleep=0.1):
        time.sleep(sleep)
        response = curl(method="post-data",
                        path=f"/v2/applications/{os.environ['BALENA_APP_ID']}"
                               "/start-service?apikey=",
                        string='{"serviceName": "%s"}' % (container_name))

        return response

    def stop(self, container_name, sleep=0.1):
        time.sleep(sleep)
        response = curl(method="post-data",
                        path=f"/v2/applications/{os.environ['BALENA_APP_ID']}"
                               "/stop-service?apikey=",
                        string='{"serviceName": "%s"}' % (container_name))

        print(self.__class__.__name__ + inspect.stack()[0][3] + " - " +
              str(response["text"]) +
              str(response["status_code"]))
        return response
