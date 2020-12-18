from flask import Flask
from flask_restful import Resource, Api
from resources.resources import portainerstart, portainerstop, portainerstatus, systeminfo, wificonnectionstatus, device, healthcheck, hostconfig, journallogs, update, uuid, wififorget, wififorgetall, wifitoggle

app = Flask(__name__)

api = Api(app)

print("Api-v1 - Starting API...")

#Configure API access points
if __name__ == '__main__':
    api.add_resource(wificonnectionstatus, '/v1/wifi/connectionstatus')
    api.add_resource(device, '/v1/device')
    api.add_resource(healthcheck, '/')
    api.add_resource(hostconfig, '/v1/hostconfig/<hostname>') 
    api.add_resource(journallogs, '/v1/journallogs')
    api.add_resource(portainerstatus, '/v1/portainer/status')
    api.add_resource(portainerstart, '/v1/portainer/start')
    api.add_resource(portainerstop, '/v1/portainer/stop')
    api.add_resource(update, '/v1/update')
    api.add_resource(uuid, '/v1/uuid')
    api.add_resource(systeminfo, '/v1/system/info')
    api.add_resource(wififorget, '/v1/wifi/forget')
    api.add_resource(wififorgetall, '/v1/wifi/forgetall')
    api.add_resource(wifitoggle, '/v1/wifitoggle')

    app.run(port=9090,host='0.0.0.0')