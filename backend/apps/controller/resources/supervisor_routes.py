import os
from common.errors import logger
from common.processes import curl
from common.processes import device_hostname
from common.processes import device_host_config
from common.processes import device_update
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class supervisor_device(Resource):
    def get(self):
        response = curl(method="get",
                        path="/v1/device?apikey=")

        return response.json(), response.status_code


class supervisor_host_config(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # Remove spaces from string and convert to lowercase
        hostname = content["hostname"].lower().replace(" ", "")

        logger.debug(f'Attempting to change hostname to {hostname}')

        response = device_host_config(hostname)

        return {'message': response.text}, response.status_code


class supervisor_hostname(Resource):
    def get(self):
        return {'hostname': str(device_hostname())}


class supervisor_journal_logs(Resource):
    def get(self):
        response = curl(method="post-json",
                        path="/v2/journal-logs?apikey=",
                        data={"follow": False, "all": True,
                              "format": "short"})

        return response.text, response.status_code


class supervisor_state(Resource):
    def get(self):
        supervisor_state = True

        response = curl(method="get",
                        path="/v2/state/status?apikey=")

        # Use requests library to parse JSON.
        json_response = response.json()

        for key in json_response['containers']:
            if key['status'].lower() != 'running':
                logger.warning("Supervisor reports container "
                               f"'{key['serviceName']}' is not in state "
                               "'Running'.")
                supervisor_state = False

        return {'message': supervisor_state}, response.status_code


class supervisor_update(Resource):
    def get(self):
        logger.info('Supervisor forced update requested')

        response = device_update(force_mode=True)

        return {'message': response.text}, response.status_code


class supervisor_uuid(Resource):
    def get(self):
        return {'supervisor_uuid': os.environ['BALENA_DEVICE_UUID']}
