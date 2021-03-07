from common.containers import container
from common.processes import curl
from flask_restful import Resource
from flask_jwt_extended import jwt_required
import os


class device(Resource):
    def get(self):

        response = curl(method="get",
                        path="/v1/device?apikey=")

        return response["json_response"], response["status_code"]


class host_config(Resource):
    @jwt_required()
    def get(self, hostname):
        response = curl(method="patch",
                        path="/v1/device/host-config?apikey=",
                        string='{"network": {"hostname": "%s"}}' % (hostname))

        return {
            'status': response["status_code"],
            'message': response["text"]
        }, response["status_code"]


class journal_logs(Resource):
    def get(self):

        response = curl(method="post-json",
                        path="/v2/journal-logs?apikey=",
                        string='("follow", "false", "all", "true", \
                            "format", "short")')

        return response["text"], response["status_code"]


class portainer_status(Resource):
    def get(self):
        response, entry = container().status(container="portainer")

        if entry["status"] == "Running":
            process_status = True
        else:
            process_status = False

        return {'status': response["status_code"],
                'running': process_status}, response["status_code"]


class portainer_start(Resource):
    @jwt_required()
    def get(self):
        response = container().start(container="portainer")

        return {'status': response["status_code"],
                'message': "OK",
                'response': response["text"]}, response["status_code"]


class portainer_stop(Resource):
    @jwt_required()
    def get(self):
        response = container().stop(container="portainer")

        return {'status': response["status_code"],
                'message': "OK",
                'response': response["text"]}, response["status_code"]


class update(Resource):
    def get(self):
        response = curl(method="post-json",
                        path="/v1/update?apikey=",
                        string='("force", "true")')

        return {'status': response["status_code"],
                'message': response["text"]}, response["status_code"]


class uuid(Resource):
    def get(self):
        return {'uuid': os.environ['BALENA_DEVICE_UUID']}
