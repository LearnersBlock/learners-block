from common.supervisor_containers import container
from common.processes import curl
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from resources.errors import print_message
import os

# Global variables
portainer_pidfile = "/app/portainer/portainer.pid"


class container_start(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        if content["container_name"] == 'portainer':
            # Create PID for portainer
            pid = str(os.getpid())
            open(portainer_pidfile, 'w').write(pid)

        response = container().start(container_name=content["container_name"])

        return {'status': response["status_code"],
                'message': response["text"]}, response["status_code"]


class container_status(Resource):
    def post(self):
        content = request.get_json()

        response, entry = container().status(
                            container_name=content["container_name"])

        try:
            if entry["status"].lower() == 'running':
                state = True
            else:
                state = False
        except Exception:
            state = True

        return {'status': response["status_code"],
                'container_status': state}, response["status_code"]


class container_stop(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        if content["container_name"] == 'portainer':
            # Delete PID for portainer
            try:
                os.remove(portainer_pidfile)
            except FileNotFoundError:
                print_message('container_stop',
                              'Portainer PID file did not exist. Continuing.')

        response = container().stop(container_name=content["container_name"])

        return {'status': response["status_code"],
                'message': response["text"]}, response["status_code"]


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
