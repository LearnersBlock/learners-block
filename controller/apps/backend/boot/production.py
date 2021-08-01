from common.processes import check_internet
from common.processes import curl
from common.wifi import wifi
from common.wifi import wifi_connect
from resources.errors import print_error
from resources.supervisor_routes import update
import subprocess
import threading
import time


def launch_wifi(self):
    # Check if already connected to Wi-Fi
    time.sleep(10)
    try:
        connected = wifi().check_connection()
    except Exception as ex:
        print_error("launch_wifi", "Error checking wifi connection. Starting \
            wifi-connect in order to allow debugging", ex)
        connected = None

    # If not connected, start Wi-Fi-Connect
    if not connected:
        try:
            # Launch Wi-Fi Connect
            wifi_connect().start()
            print('Api-v1 - API Started - Launched wifi-connect.')
        except Exception as ex:
            print_error("launch_wifi",
                        'Wifi-connect failed to launch.', ex)

    # If internet available (ethernet or WiFi) request update
    if check_internet():
        try:
            update().get()
            print('Api-v1 - API Started - Internet available, '
                  'software update request made.')
        except Exception as ex:
            print_error("launch_wifi", 'Software update failed.', ex)


def startup(self):
    # Check hostname in container is correct
    try:
        # Fetch container hostname and device hostname
        container_hostname = subprocess.run(["hostname"], capture_output=True,
                                            check=True,
                                            text=True).stdout.rstrip()

        device_hostname = curl(method="get",
                               path="/v1/device/host-config?apikey=",
                               supervisor_retries=20)

        # Check container and device hostname match
        if container_hostname != \
                device_hostname["json_response"]["network"]["hostname"]:
            print("Api-v1 - Container hostname and device hostname do not "
                  "match. Likely a hostname change has been performed. Balena "
                  "Supervisor should detect this and rebuild the container "
                  "shortly. Waiting 30 seconds before continuing anyway.")
            time.sleep(30)

    except Exception as ex:
        print_error("startup",
                    'Failed to compare hostnames, starting anyway.', ex)

    # If connected to a wifi network then update device,
    # otherwise launch wifi-connect
    try:
        wifi_thread = threading.Thread(target=launch_wifi,
                                       args=(1,),
                                       name='wifi_thread')
        wifi_thread.start()

    except Exception as ex:
        print_error("startup",
                    'Failed during launch. Continuing for debug.', ex)
