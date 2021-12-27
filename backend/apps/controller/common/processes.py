import config
import datetime
import os
import requests
import shutil
import signal
import socket
import subprocess
import time
from common.errors import logger
from common.errors import SupervisorCurlFailed
from common.errors import SupervisorUnreachable
from flask_restful import abort
import ntplib


# Initiate NTP Library
ntp = ntplib.NTPClient()


def check_connection():
    try:
        run = subprocess.run(["iw", "dev", "wlan0", "link"],
                             capture_output=True,
                             text=True).stdout.rstrip()
    except Exception:
        logger.exception("Failed checking connection. Returning False to"
                         "allow continuing.")
        return False

    if run.lower()[:13] == "not connected":
        return False
    else:
        return True


def check_internet(host="8.8.8.8", port=53, timeout=5):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        # If there is a connection return True
        return True
    except socket.error:
        # If there isn't a connection return False
        return False


def check_space():
    _, _, free = shutil.disk_usage("/")
    if free <= 100000000:
        return True
    return False


def check_supervisor(supervisor_retries, timeout):
    # Check Balena Supervisor is ready
    retry = 1

    while True:
        try:
            supervisor_status = requests.get(
                f'{os.environ["BALENA_SUPERVISOR_ADDRESS"]}/ping',
                timeout=timeout
            )

            if supervisor_status.status_code == 200:
                break

        except Exception:
            logger.info('Waiting for Balena Supervisor to be ready. '
                        f'Retry {str(retry)}.')

            if retry == supervisor_retries:
                logger.error('Supervisor could not be reached.')
                raise SupervisorUnreachable

            time.sleep(2)
            retry = retry + 1

    return {'message': 'Supervisor up'}


# Check chronyd has executed before. Used as a useful indicator of whether
# this is the first ever connection to the internet.
def chronyd_check(func):
    def inner(*args, **kwargs):
        if not config.dev_mode and not config.chronyd_synced:
            try:
                subprocess.check_output("chronyc sources | grep '*'",
                                        shell=True)
                config.chronyd_synced = True
            except Exception:
                logger.exception('ChronyD not synced yet.')
                abort(502,
                      status=502,
                      message='System is still syncing. Try again later.')
        return func(*args, **kwargs)
    return inner


def container_hostname():
    return subprocess.run(["hostname"],
                          capture_output=True,
                          check=True,
                          text=True).stdout.rstrip()


def curl(supervisor_retries=8, timeout=5, **cmd):
    check_supervisor(supervisor_retries, timeout)

    logger.debug(f"Curl commands = {cmd}")

    # Process curl requests
    try:
        path = os.environ["BALENA_SUPERVISOR_ADDRESS"] + cmd["path"] + \
            os.environ["BALENA_SUPERVISOR_API_KEY"]

        # Post method
        if cmd["method"] == 'post-json':
            response = requests.post(
                path,
                json=cmd["data"],
                timeout=timeout
            )

        # Patch method
        elif cmd["method"] == 'patch':
            response = requests.patch(
                path,
                json=cmd["data"],
                timeout=timeout
            )

        # Get method
        elif cmd["method"] == 'get':
            response = requests.get(
                path,
                timeout=timeout
            )
    except Exception:
        logger.exception("Supervisor curl request error.")
        raise SupervisorCurlFailed

    try:
        response.raise_for_status()
    except Exception:
        logger.exception('Failed to send request to Supervisor')
        raise SupervisorCurlFailed

    # Return response
    return response


def device_host_config(hostname, **kwargs):
    new_hostname = curl(method="patch",
                        path="/v1/device/host-config?apikey=",
                        data={"network": {"hostname": hostname}},
                        **kwargs)

    return new_hostname


def device_hostname(**kwargs):
    device_hostname = curl(method="get",
                           path="/v1/device/host-config?apikey=",
                           **kwargs).json()

    return device_hostname["network"]["hostname"]


def database_recover():
    # Resetting database
    logger.error("Database error. Deleting database and restarting.")

    try:
        # If the container hostname is not the default, remove
        # the run.pid to false it back to default on next boot
        if container_hostname() is not config.default_hostname:
            hostname_reset()

    except Exception:
        logger.exception('Failed to delete run.pid. Continuing...')

    # Rename the .db file. A new one will be rebuilt fresh on next boot.
    # While this is a drastic step, it ensures devices do not
    # get bricked in the field.
    try:
        path = os.path.realpath('.') + "/db/"

        os.rename(path + "sqlite.db",
                  path + f"sqlite.db - {str(datetime.datetime.now())}")

        os.kill(os.getpid(), signal.SIGTERM)
    except Exception:
        logger.exception("Failed to delete the database.")


def hostname_reset():
    # Remove run.pid to force reset of hostname
    if not config.dev_mode:
        try:
            os.remove('/app/db/run.pid')
        except Exception:
            logger.exception('Failed deleting run.pid')


def human_size(nbytes):
    # Convert system file sizes to human readable
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def led(mode):
    # Activate LED on compatible devices
    # 1 = on
    # 0 = off
    try:
        with open('/sys/class/leds/led0/brightness', 'w+') as f:
            f.write(str(mode))
    except Exception:
        # This is not possible on some devices.
        pass


# Check time has been synced before request decorator
def ntp_check(func):
    def inner(*args, **kwargs):
        # Only trigger if there is an internet connection
        if check_internet():
            try:
                # Check if the system clock is in sync otherwise Docker Hub
                # certificates create an error
                time_offset = ntp.request('time.cloudflare.com',
                                          version=3).offset
                logger.info(f"Time offset is: {time_offset}")
                if time_offset > 3600 or time_offset < -3600:
                    logger.debug('Not in sync with NTP server.')
                    abort(502,
                          status=502,
                          message='System is still loading. Try again later.')
            except Exception:
                logger.exception('Failed to check time with NTP server.')
                # In event of connection error, allowing Docker to try anyway.

        return func(*args, **kwargs)

    return inner
