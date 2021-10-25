from common.errors import logger
from common.processes import check_internet
from common.processes import curl
from common.wifi import wifi
from resources.supervisor_routes import supervisor_update
import config
import subprocess
import sys
import threading
import time


def dnsmasq():
    DEFAULT_GATEWAY = "192.168.42.1"
    DEFAULT_DHCP_RANGE = "192.168.42.2,192.168.42.254"
    DEFAULT_INTERFACE = "wlan0"  # use 'ip link show' to see list of interfaces

    # Build the list of args
    path = "/usr/sbin/dnsmasq"
    args = [path]
    args.append(f"--address=/#/{DEFAULT_GATEWAY}")
    args.append(f"--dhcp-range={DEFAULT_DHCP_RANGE}")
    args.append(f"--dhcp-option=option:router,{DEFAULT_GATEWAY}")
    args.append(f"--interface={DEFAULT_INTERFACE}")
    args.append("--keep-in-foreground")
    args.append("--bind-dynamic")
    args.append("--except-interface=lo")
    args.append("--conf-file")
    args.append("--no-hosts")

    try:
        subprocess.Popen(args)
    except Exception as ex:
        logger.exception('Failed to start dnsmasq.')
        return ex

    return True


def handle_exit(*args):
    # Ensure Wi-Fi connections are shutdown softly
    try:
        wifi.forget(conn_name=config.hotspot_name)
    except Exception:
        logger.exception('Failed to terminate wifi processes.')

    logger.info('Finshed the exit process.')


def handle_sigterm(*args):
    sys.exit(0)


def launch_wifi(self):
    # Delay to allow a pre-configured connection to connect
    time.sleep(10)

    # Check if already connected to Wi-Fi
    try:
        connected = wifi.check_connection()
    except Exception:
        logger.exception('Error checking wifi connection. Starting \
            wifi-connect in order to allow debugging')
        connected = None

    # If not connected, start Wi-Fi-Connect
    if not connected:
        try:
            # Launch Wi-Fi Connect
            wifi.start_hotspot()
            logger.info("Api-v1 - API Started - Launched wifi-connect.")
        except Exception:
            logger.exception('Wifi-connect failed to launch')

    # If internet available (Ethernet or Wi-Fi) request update
    if check_internet():
        try:
            supervisor_update().get()
            logger.info('Api-v1 - API Started - Internet available, '
                        'software update request made.')
        except Exception:
            logger.exception('Software update failed.')


def startup():
    # Check hostname in container is same as device
    try:
        # Fetch container hostname
        container_hostname = subprocess.run(["hostname"], capture_output=True,
                                            check=True,
                                            text=True).stdout.rstrip()

        # Fetch device hostname from Balena Supervisor
        device_hostname = curl(method="get",
                               path="/v1/device/host-config?apikey=",
                               supervisor_retries=20)

        # Check container and device hostname match
        if container_hostname != \
                device_hostname["json_response"]["network"]["hostname"]:
            logger.info("Api-v1 - Container hostname and device hostname do "
                        "not match. Likely a hostname change has been "
                        "performed. Balena Supervisor should detect this "
                        "and rebuild the container shortly. Waiting 30"
                        "seconds before continuing anyway.")
            time.sleep(30)

    except Exception:
        logger.exception('Failed to compare hostnames, starting anyway.')

    # Start dnsmasq permanently
    start_dnsmasq = dnsmasq()
    if start_dnsmasq is not True:
        logger.info("dnsmasq failed to start. " + start_dnsmasq)

    # Start the launch_wifi process as a thread to avoid delays
    # to booting device
    try:
        wifi_thread = threading.Thread(target=launch_wifi,
                                       args=(1,),
                                       name='wifi_thread')
        wifi_thread.start()

    except Exception:
        logger.exception("Failed during wifi_thread. Continuing for debug.")
