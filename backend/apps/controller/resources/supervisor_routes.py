import os
from common.errors import logger
from common.processes import curl
from common.processes import device_host_config
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class supervisor_device(Resource):
    def get(self):
        response = curl(method="get",
                        path="/v1/device?apikey=")

        return response["json_response"], response["status_code"]


class supervisor_host_config(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # Remove spaces from string and convert to lowercase
        hostname = content["hostname"].lower().replace(" ", "")

        logger.debug(f'Attempting to change hostname to {hostname}')

        response = device_host_config(hostname)

        return {'status': response["status_code"],
                'message': response["message"]}, response["status_code"]


class supervisor_journal_logs(Resource):
    def get(self):
        response = curl(method="post-json",
                        path="/v2/journal-logs?apikey=",
                        string='("follow", "false", "all", "true", \
                            "format", "short")')

        return response["message"], response["status_code"]


class supervisor_update(Resource):
    def get(self):
        logger.debug('Supervisor update requested.')

        response = curl(method="post-json",
                        path="/v1/update?apikey=",
                        string='("force", "true")')

        return {'status': response["status_code"],
                'message': response["message"]}, response["status_code"]


class supervisor_uuid(Resource):
    def get(self):
        return {'supervisor_uuid': os.environ['BALENA_DEVICE_UUID']}
