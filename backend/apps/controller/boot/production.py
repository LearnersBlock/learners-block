import subprocess
import sys
import threading
import time
from common.errors import logger
from common.processes import check_connection
from common.processes import check_internet
from common.processes import container_hostname
from common.processes import device_hostname
from common.processes import device_update
from common.processes import led
from common.wifi import wifi


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
    except Exception:
        logger.exception('Failed to start dnsmasq.')
        # Allow pass to facilitate software updates


def handle_exit(*args):
    logger.info('Finshed the exit process.')


def handle_sigterm(*args):
    sys.exit(0)


def launch_wifi(self):
    # Delay to allow a pre-configured connection to connect
    time.sleep(10)

    # If the Wi-Fi connection or device is already active, do nothing
    if check_connection() or wifi.check_device_state():
        led(1)
    else:
        led(0)
        wifi.refresh_networks(retries=1)
        wifi.connect()
        logger.info("Api-v1 - API Started - Launched wifi-connect.")

    # If internet available (Ethernet or Wi-Fi) request update
    if check_internet():
        try:
            device_update(force_mode=False)
        except Exception:
            logger.exception('Software update failed.')


def startup():
    # Check hostname in container is same as device
    try:
        # Check container and device hostname match
        if container_hostname() != \
                device_hostname(supervisor_retries=20):
            logger.warning("Api-v1 - Container hostname and device hostname "
                           "do not match. A short delay here allows time for  "
                           "Supervisor to restart the container if necessary.")
            time.sleep(30)

    except Exception:
        logger.exception('Failed to compare hostnames.')
        # Starting anyway to allow debugging

    # Start dnsmasq permanently
    dnsmasq()

    # Start the launch_wifi process as a thread to avoid delays
    # to booting device
    wifi_thread = threading.Thread(target=launch_wifi,
                                   args=(1,),
                                   name='wifi_thread')
    wifi_thread.start()
