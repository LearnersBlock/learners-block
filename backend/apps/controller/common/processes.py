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
                headers={"Content-Type": "application/json"}, timeout=timeout
            )

            if supervisor_status.status_code == 200:
                break
            else:
                abort(supervisor_status.status_code,
                      status=supervisor_status.status_code,
                      message='Supervisor returned error code.',
                      error=str(supervisor_status.text))

        except Exception:
            logger.info(f'Waiting for Balena Supervisor to be ready. '
                        f'Retry {str(retry)}.')

            if retry == supervisor_retries:
                logger.error('Supervisor could not be reached.')
                raise SupervisorUnreachable

            time.sleep(2)
            retry = retry + 1

    return {'status': 200, 'message': 'Supervisor up'}


def curl(supervisor_retries=8, timeout=5, **cmd):
    check_supervisor(supervisor_retries, timeout)

    logger.debug(f"Curl commands = {cmd}")

    # Process curl request
    try:
        if cmd["method"] == 'post-json':
            response = requests.post(
                f'{os.environ["BALENA_SUPERVISOR_ADDRESS"]}{cmd["path"]}'
                f'{os.environ["BALENA_SUPERVISOR_API_KEY"]}',
                json=[cmd["string"]],
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )

        elif cmd["method"] == 'post-data':
            response = requests.post(
                f'{os.environ["BALENA_SUPERVISOR_ADDRESS"]}{cmd["path"]}'
                f'{os.environ["BALENA_SUPERVISOR_API_KEY"]}',
                data=cmd["string"],
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )

        elif cmd["method"] == 'patch':
            response = requests.patch(
                f'{os.environ["BALENA_SUPERVISOR_ADDRESS"]}{cmd["path"]}'
                f'{os.environ["BALENA_SUPERVISOR_API_KEY"]}',
                data=cmd["string"],
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )

        elif cmd["method"] == 'get':
            response = requests.get(
                f'{os.environ["BALENA_SUPERVISOR_ADDRESS"]}{cmd["path"]}'
                f'{os.environ["BALENA_SUPERVISOR_API_KEY"]}',
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )
    except Exception:
        logger.exception("Supervisor curl request timed out.")
        raise SupervisorCurlFailed

    # Check if response is JSON and if not return it as text
    try:
        response.json()
    except Exception:
        # Return successful JSON response
        return {"status_code": response.status_code,
                "message": response.text}

    logger.debug(f"Curl request: {response.status_code}")

    # Return non-JSON response
    return {"status_code": response.status_code,
            "message": response.text,
            "json_response": response.json()}


def database_recover():
    # Resetting database
    logger.warning("Database error. Deleting database and restarting.")

    try:
        # Get current hostname
        container_hostname = subprocess.run(["hostname"],
                                            capture_output=True,
                                            check=True,
                                            text=True).stdout.rstrip()

        # If the container hostname is not the default, remove
        # the run.pid to false it back to default on next boot
        if container_hostname is not config.default_hostname:
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
