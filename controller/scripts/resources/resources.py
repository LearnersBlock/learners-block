from flask_restful import abort, request, Resource
from werkzeug import serving
from resources.processes import container, curl, human_size, wifi
import resources.globals
import shutil
import threading

# Disable logging for health_check
parent_log_request = serving.WSGIRequestHandler.log_request

# Restrict certain calls to API use only
def check_permission():
    try: 
        if request.remote_addr[:4] != "172.":
            abort(403)  # Forbidden
    except Exception:
        pass

def log_request(self, *args, **kwargs):
    if self.path == '/':
        return

    parent_log_request(self, *args, **kwargs)


class device(Resource):
    def get(self):

        response = curl(method="get",
                        path="/v1/device?apikey=")

        return response["json_response"], response["status_code"]


class health_check(Resource):
    def get(self):

        serving.WSGIRequestHandler.log_request = log_request
        return {'status': 200, 'message': 'ok'}, 200


class host_config(Resource):
    def get(self, hostname):

        check_permission()

        response = curl(method="patch",
                        path="/v1/device/host-config?apikey=",
                        string='{"network": {"hostname": "%s"}}' % (hostname))

        return {
            'status': response["status_code"],
            'hostname': hostname,
            'message': response["text"]
        }, response["status_code"]


class journal_logs(Resource):
    def get(self):

        response = curl(method="post-json",
                        path="/v2/journal-logs?apikey=",
                        string='("follow", "false", "all", "true", "format", "short")')

        return response["text"], response["status_code"]


class portainer_status(Resource):
    def get(self):

        check_permission()

        response, entry = container().status(container="portainer")

        return {'status': response["status_code"], 'message': entry["status"]}, response["status_code"]


class portainer_start(Resource):
    def get(self):

        check_permission()

        response = container().start(container="portainer")

        return {'status': response["status_code"], 'message': response["text"]}, response["status_code"]


class portainer_exit(Resource):
    def get(self):

        check_permission()

        response = container().stop(container="portainer")

        return {'status': response["status_code"], 'message': response["text"]}, response["status_code"]


class update(Resource):
    def get(self):
        response = curl(method="post-json",
                        path="/v1/update?apikey=",
                        string='("force", "true")')

        return {'status': response["status_code"], 'message': response["text"]}, response["status_code"]


class uuid(Resource):
    def get(self):
        return {'uuid': resources.globals.BALENA_DEVICE_UUID}


class system_info(Resource):
    def get(self):
        return {"storage": {
                    'total': human_size(shutil.disk_usage("/tmp")[-0]),
                    'available': human_size(shutil.disk_usage("/tmp")[-1])
                },
                "versions": {
                    'lb': resources.globals.VER
                    }
               }


class wifi_connection_status(Resource):
    def get(self):
        response = wifi().check_connection()

        if response:
            return {'status': 200, 'message': 'connected'}, 200
        else:
            return {'status': 206, 'message': 'disconnected'}, 206


class wifi_forget(Resource):
    def get(self):

        check_permission()

        # Check and store the current connection state
        connection_state = wifi().check_connection()

        # If the device is connected to a wifi network
        if not connection_state:
            return {
                'status': 409,
                'message': 'Device is already disconnected, connection cannot be reset.'
            }, 409

        wifi_forget = threading.Thread(target=wifi.forget, args=(1,), name='wifi_forget')
        wifi_forget.start()

        return {'status': 202, 'message': 'Reset request sent.'}, 202


class wifi_forget_all(Resource):
    def get(self):

        check_permission()

        wifi_forget_all = threading.Thread(target=wifi.forget_all, args=(1,), name='wifi_forget_all')
        wifi_forget_all.start()

        return {'status': 202, 'message': 'Reset request sent.'}, 202
