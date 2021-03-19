from common.processes import curl
from common.wifi import handle_exit
from common.wifi import wifi
from common.wifi import wifi_connect
from common.containers import container
from resources.supervisor_routes import update
import inspect
import subprocess
import threading
import time
import atexit
import signal


# Function for first launch called by 'startup' function
def launch_wifi():
    # Check if already connected to Wi-Fi
    time.sleep(20)
    try:
        connected = wifi().check_connection()
    except Exception as ex:
        print("Api-v1 - Error checking wifi connection. Starting wifi-connect "
              "in order to allow debugging. " +
              inspect.stack()[0][3] + " - " + str(ex))
        connected = None

    # If connected, perform container updatem if not, start Wi-Fi Connect
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
            wifi_connect().start()
            response = "Api-v1 - API Started - Launched wifi-connect."
        except Exception as ex:
            response = ("Wifi-connect failed to launch. " +
                        inspect.stack()[0][3] +
                        " - " + str(ex))

    print(response)
    return response


def hostname_check():
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
            time.sleep(60)

    except Exception as ex:
        print("Api-v1 - Failed to compare hostnames, starting anyway: "
              + inspect.stack()[0][3] +
              " - " + str(ex))


def portainer_check():
    # Stop portainer on boot
    # String cannot be portainer_stop due to clash with endpoint
    try:
        portainer_exit = threading.Thread(target=container.stop,
                                          args=(None, "portainer", 10),
                                          name='portainer_exit')
        portainer_exit.start()

    except Exception as ex:
        print("Failed to stop Portainer. " +
              " - " + inspect.stack()[0][3] + " - " + str(ex))


def startup():
    # If connected to a wifi network then update device,
    # otherwise launch wifi-connect
    try:
        device_start = threading.Thread(target=launch_wifi,
                                        args=(1,),
                                        name='device_start')
        device_start.start()

    except Exception as ex:
        print("Failed during launch. Continuing for debug. " +
              inspect.stack()[0][3] + " - " + str(ex))

    # Ensure soft shutdown to term wifi-connect
    atexit.register(handle_exit, None, None)
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)

    # Check portainer status on boot
    portainer_check()

    # Check hostnames are set correctly
    hostname_check()

    # Start app
    startup()
