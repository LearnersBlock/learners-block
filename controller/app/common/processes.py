from flask_restful import abort
import requests
import os
import time
import sys


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
            print(f'Waiting for Balena Supervisor to be ready. \
                    {str(ex)}. Retry {str(retry)}.')

            if retry == supervisor_retries:
                abort(408, status=408,
                      message=str(ex).rstrip())

            time.sleep(2)
            retry = retry + 1

    return {'status': 200, 'message': 'Supervisor up'}, 200


def curl(supervisor_retries=8, timeout=5, **cmd):
    check_supervisor(supervisor_retries, timeout)

    # Process curl request
    try:
        if cmd["method"] == 'post-json':
            response = requests.post(
                f'{os.environ["BALENA_SUPERVISOR_ADDRESS"]}{cmd["path"]} \
                {os.environ["BALENA_SUPERVISOR_API_KEY"]}',
                json=[cmd["string"]],
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )

        elif cmd["method"] == 'post-data':
            response = requests.post(
                f'{os.environ["BALENA_SUPERVISOR_ADDRESS"]}{cmd["path"]} \
                {os.environ["BALENA_SUPERVISOR_API_KEY"]}',
                data=cmd["string"],
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )

        elif cmd["method"] == 'patch':

            response = requests.patch(
                f'{os.environ["BALENA_SUPERVISOR_ADDRESS"]}{cmd["path"]} \
                {os.environ["BALENA_SUPERVISOR_API_KEY"]}',
                data=cmd["string"],
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )

        elif cmd["method"] == 'get':

            response = requests.get(
                f'{os.environ["BALENA_SUPERVISOR_ADDRESS"]}{cmd["path"]} \
                {os.environ["BALENA_SUPERVISOR_API_KEY"]}',
                headers={"Content-Type": "application/json"},
                timeout=timeout
            )
    except Exception as ex:
        print("Curl request timed out. " + str(ex))
        abort(408, status=408,
              message=str(ex).rstrip())

    try:
        response.json()
    except Exception:
        return {"status_code": response.status_code, "text": response.text}

    return {"status_code": response.status_code, "text": response.text,
            "json_response": response.json()}


def handle_exit(*args):
    try:
        try:
            global wifi_process
            wifi_process.terminate()
            wifi_process.communicate(timeout=10)
        except Exception:
            wifi_process.kill()
    except Exception as ex:
        print("Wifi-connect was already down. " + str(ex))
    print("Finshed the exit process")
    sys.exit(0)


def human_size(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])
