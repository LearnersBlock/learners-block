from common.processes import curl
from common.wifi import wifi
from common.wifi import wifi_connect
from common.containers import container
from resources.supervisor_routes import update
import inspect
import subprocess
import threading
import time


# Function for first launch called by 'startup' function
def launch_wifi(self):
    # Check if already connected to Wi-Fi
    time.sleep(10)
    try:
        connected = wifi().check_connection()
    except Exception as ex:
        print("Api-v1 - Error checking wifi connection. Starting wifi-connect "
              "in order to allow debugging. " +
              inspect.stack()[0][3] + " - " + str(ex))
        connected = None

    # If connected, perform container update, if not, start Wi-Fi Connect
    if connected:
        try:
            update().get()
            response = ('Api-v1 - API Started - Device already connected to '
                        'local wifi, software update request made.')
        except Exception as ex:
            response = ("Software update failed. " +
                        " - " + inspect.stack()[0][3] + " - " + str(ex))
    else:
        try:
            # Refresh networks in area before launch
            print("Refreshing network points")

            subprocess.run(
                ["iw", "wlan0", "scan"],
                capture_output=True,
                text=True).stdout.rstrip()

            # Launch Wi-Fi Connect
            wifi_connect().start()
            response = "Api-v1 - API Started - Launched wifi-connect."
        except Exception as ex:
            response = ("Wifi-connect failed to launch. " +
                        inspect.stack()[0][3] +
                        " - " + str(ex))

    print(response)
    return response


def startup():
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
                  "shortly. Waiting 60 seconds before continuing anyway.")
            time.sleep(30)

    except Exception as ex:
        print("Api-v1 - Failed to compare hostnames, starting anyway: "
              + inspect.stack()[0][3] +
              " - " + str(ex))

    # If connected to a wifi network then update device,
    # otherwise launch wifi-connect
    try:
        wifi_thread = threading.Thread(target=launch_wifi,
                                       args=(1,),
                                       name='wifi_thread')
        wifi_thread.start()

    except Exception as ex:
        print("Failed during launch. Continuing for debug. " +
              inspect.stack()[0][3] + " - " + str(ex))

    # Stop portainer on boot
    try:
        portainer_exit = threading.Thread(target=container.stop,
                                          args=(None, "portainer", 10),
                                          name='portainer_exit')
        portainer_exit.start()

    except Exception as ex:
        print("Failed to stop Portainer. " +
              " - " + inspect.stack()[0][3] + " - " + str(ex))
