from common.system_processes import curl
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
import os


class device(Resource):
    def get(self):
        response = curl(method="get",
                        path="/v1/device?apikey=")

        return response["json_response"], response["status_code"]


class host_config(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        response = curl(method="patch",
                        path="/v1/device/host-config?apikey=",
                        string='{"network": {"hostname": "%s"}}' %
                        (content["hostname"]))

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
