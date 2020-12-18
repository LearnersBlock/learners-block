from flask_restful import Resource
from werkzeug import serving
import shutil
import time

wifistatus = "down"

#Disable logging for healthcheck
parent_log_request = serving.WSGIRequestHandler.log_request

def log_request(self, *args, **kwargs):
    if self.path == '/':
        return

    parent_log_request(self, *args, **kwargs)

def humansize(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

class device(Resource):
    def get(self):

        return {'response': 'output'}, 200

class healthcheck(Resource):
    def get(self):
        serving.WSGIRequestHandler.log_request = log_request
        return {'status': 200, 'message': 'ok'}, 200

class hostconfig(Resource):
    def get(self, hostname):

        return {
            'status': 200,
            'hostname': hostname,
            'message': f'Hostname was updated to {hostname}'
        }, 200

# /v1/journallogs
class journallogs(Resource):
    def get(self):

        return "journal logs"


class portainerstatus(Resource):
    def get(self):
 
        return {'status': 200, 'message': "Running"}, 200


class portainerstart(Resource):
    def get(self):

        return {'status': 200, 'message': 'OK'}, 200


class portainerstop(Resource):
    def get(self):

        time.sleep(10)

        return {'status': 200, 'message': 'OK'}, 200


# /v1/update
class update(Resource):
    def get(self):

        return {'status': 202, 'message': "Accepted"}, 202

# /v1/uuid
class uuid(Resource):
    def get(self):

        return {'uuid': "asdsadsdf213qs2"}


class systeminfo(Resource):
    def get(self):
        return {"storage": {
                    'total': humansize(shutil.disk_usage("/tmp")[-0]),
                    'available': humansize(shutil.disk_usage("/tmp")[-1])
                },
                "versions": {
                    "lb": "0.0.1",
                    "frontend": "0.0.1",
                    "backend": "0.0.1",
                    "controller": "0.0.1",
                    "file_manager": "0.0.1",
                    "wificonnect_ui": "0.0.1"
                }
               }


# Network Endpoints
# /v1/wificonnectionstatus
class wificonnectionstatus(Resource):
    def get(self):

        if wifistatus == "up":
            return {
                'status': 200,
                'message': 'connected'
            }, 200

        return {
            'status': 206,
            'message': 'disconnected'
        }, 206

# /v1/wifitoggle
class wifitoggle(Resource):
    def get(self):

        global wifistatus

        if wifistatus == "down":
            print("WiFi is now up", flush=True)
            wifistatus = "up"

        elif wifistatus == "up":
            print("WiFi is now down", flush=True)
            wifistatus = "down"

        return "This is a temporary path, not for production. Wifi is now set to " + wifistatus 

# /v1/wififorget
class wififorget(Resource):
    def get(self):

        global wifistatus

        if wifistatus == "down":
            return {
                'status': 409,
                'message': 'Device is already disconnected, connection cannot be reset.'
            }, 409

        wifitoggle().get()

        return {'status': 202, 'message': 'Reset request sent.'}, 202  

# /v1/wififorgetall
class wififorgetall(Resource):
    def get(self):

        global wifistatus
        
        if wifistatus == "up":
            wifitoggle().get()

        return {'status': 202, 'message': 'Reset request sent.'}, 202
        