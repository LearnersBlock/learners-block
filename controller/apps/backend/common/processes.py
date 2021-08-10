from flask_restful import abort
from resources.errors import print_message
import os
import requests
import shutil
import socket
import time


def check_space():
    _, _, free = shutil.disk_usage("/tmp")
    if free <= 100000000:
        return True
    return False


def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print_message('check_internet', 'internet check failure', ex)
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
                      message='Supervisor returned error code.')

        except Exception as ex:
            print(f'Waiting for Balena Supervisor to be ready. '
                  f'Retry {str(retry)}.')

            if retry == supervisor_retries:
                abort(408, status=408,
                      message=str(ex))

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
        print_message('curl', 'Curl request timed out', ex)
        abort(408, status=408,
              message=str(ex))

    # Check if response is JSON and if not return it as text
    try:
        response.json()
    except Exception:
        return {"status_code": response.status_code, "text": response.text}

    return {"status_code": response.status_code, "text": response.text,
            "json_response": response.json()}


def database_recover():
    # Adding delay to allow user intervetion to abort
    print_message('database_recover', 'Database error detected. '
                  'Waiting 60 seconds before deleting '
                  'database and restarting.')
    time.sleep(60)

    # Remove the .db file. It will be rebuilt fresh on next boot.
    # While this is a drastic step, it ensures devices do not
    # get bricked in the field.
    try:
        os.remove(os.path.realpath('.') + "/db/sqlite.db")
    except Exception as ex:
        print_message('database_recover', 'Failed to delete the database. '
                      'File may be missing.', ex)


def demote(user_uid, user_gid):
    # Demote the user to pass UID/GID for one subprocess only
    def set_ids():
        os.setgid(user_gid)
        os.setuid(user_uid)

    return set_ids


def human_size(nbytes):
    # Convert system file sizes to human readable
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])
