import config
import datetime
import os
import requests
import secrets
import shutil
import signal
import socket
import subprocess
import time
from common.errors import logger
from dotenv import dotenv_values
from flask_restful import abort


def check_connection():
    try:
        run = subprocess.run(["iw", "dev", "wlan0", "link"],
                             capture_output=True,
                             text=True).stdout.rstrip()
    except Exception:
        logger.exception("Failed checking connection. Returning False.")
        return False

    if run.lower()[:13] == "not connected":
        return False
    else:
        return True


def check_internet(host="8.8.8.8", port=53, timeout=6):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
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

        except Exception as ex:
            logger.info(f'Waiting for Balena Supervisor to be ready. '
                        f'Retry {str(retry)}.')

            if retry == supervisor_retries:
                abort(408, status=408,
                      message='Supervisor unavailable.',
                      error=str(ex))

            time.sleep(2)
            retry = retry + 1

    return {'status': 200, 'message': 'Supervisor up'}


def curl(supervisor_retries=8, timeout=5, **cmd):
    check_supervisor(supervisor_retries, timeout)

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
    except Exception as ex:
        logger.exception("Curl request timed out.")
        abort(408,
              status=408,
              message='Curl request failed',
              error=str(ex))

    # Check if response is JSON and if not return it as text
    try:
        response.json()
    except Exception:
        return {"status_code": response.status_code, "message": response.text}

    logger.debug(f"Curl request: {response.status_code}")

    return {"status_code": response.status_code, "message": response.text,
            "json_response": response.json()}


def database_recover():
    # Resetting database
    logger.warning("Deleting database and restarting.")

    try:
        # Get current hostname
        container_hostname = subprocess.run(["hostname"],
                                            capture_output=True,
                                            check=True,
                                            text=True).stdout.rstrip()

        # If the container hostname is not the default, remove
        # the run.pid to false it back to default on next boot
        if container_hostname is not config.default_hostname:
            os.remove('/app/db/run.pid')
    except Exception:
        logger.exception('Failed to delete run.pid. Continuing...')
        pass

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


# Fetch the secret key or generate one if it is absent
def get_secret_key():
    # Generate secret key
    if not dotenv_values("db/.secret_key"):
        with open('./db/.secret_key', 'w') as secrets_file:
            secrets_file.write("SECRET_KEY = " + secrets.token_hex(32))
    key = dotenv_values("./db/.secret_key")
    return key["SECRET_KEY"]


def human_size(nbytes):
    # Convert system file sizes to human readable
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])
