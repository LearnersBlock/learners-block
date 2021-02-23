from flask import Flask
from flask_restful import Api
from resources.resources import device, health_check, host_config, journal_logs, portainer_status, \
portainer_start, portainer_exit, system_info, update, uuid, wifi_connection_status, wifi_forget, wifi_forget_all
from resources.processes import container, curl, wifi, wifi_connect
import resources.globals
import atexit
import signal
import subprocess
import threading
import time

app = Flask(__name__)

api = Api(app)

print("Api-v1 - Starting API...")

def launch(self):
    time.sleep(20)
    try:
        connected = wifi().check_connection()
    except Exception as ex:
        print("Api-v1 - Error checking wifi connection. Starting wifi-connect in order to allow debugging. " + str(ex))
        connected = None

    if connected:
        try:
            update().get()
            response = "Api-v1 - API Started - Device already connected to local wifi, software update request made."
        except Exception as ex:
            response = "Software update failed. " + str(ex)
    else:
        try:
            wifi_connect().start()
            response = "Api-v1 - API Started - Launched wifi-connect."
        except Exception as ex:
            response = "Wifi-connect failed to launch. " + str(ex)

    print(response)
    return response

# Stop portainer on boot
try:
    portainer_stop = threading.Thread(target=container.stop, args=(None,"portainer",10), name='portainer_stop')
    portainer_stop.start()

except Exception as ex:
    print("Failed to stop Portainer. " + str(ex))

# Check hostname in container is correct
try:
    # Fetch container hostname and device hostname
    container_hostname = subprocess.run(["hostname"], capture_output=True, text=True).stdout.rstrip()
    device_hostname = curl(method="get", path="/v1/device/host-config?apikey=", supervisor_retries=20)

    # Check container and device hostname match
    if container_hostname != device_hostname["json_response"]["network"]["hostname"]:
        print("Api-v1 - Container hostname and device hostname do not match. Likely a hostname \
        change has been performed. Balena Supervisor should detect this and rebuild \
        the container shortly. Waiting 60 seconds before continuing anyway.")
        time.sleep(60)

except Exception as ex:
    print("Api-v1 - Failed to compare hostnames, starting anyway: " + str(ex)) 

# If connected to a wifi network then update device, otherwise launch wifi-connect
try:
    device_start = threading.Thread(target=launch, args=(1,), name='device_start')
    device_start.start()

except Exception as ex:
    print("Failed during launch. Continuing for debug. " + str(ex))

atexit.register(resources.processes.handle_exit, None, None)
signal.signal(signal.SIGTERM, resources.processes.handle_exit)
signal.signal(signal.SIGINT, resources.processes.handle_exit)

# Configure API access points
if __name__ == '__main__':
    api.add_resource(wifi_connection_status, '/v1/wifi/connectionstatus')
    api.add_resource(device, '/v1/device')
    api.add_resource(health_check, '/')
    api.add_resource(host_config, '/v1/hostconfig/<hostname>')
    api.add_resource(journal_logs, '/v1/journallogs')
    api.add_resource(portainer_status, '/v1/portainer/status')
    api.add_resource(portainer_start, '/v1/portainer/start')
    api.add_resource(portainer_exit, '/v1/portainer/stop')
    api.add_resource(system_info, '/v1/system/info')
    api.add_resource(update, '/v1/update')
    api.add_resource(uuid, '/v1/uuid')
    api.add_resource(wifi_forget, '/v1/wifi/forget')
    api.add_resource(wifi_forget_all, '/v1/wifi/forget_all')

    app.run(port=9090, host='0.0.0.0')
