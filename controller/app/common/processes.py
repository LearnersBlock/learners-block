from flask_restful import abort
import json
import os
import requests
import shutil
import subprocess
import sys
import time

# Set defalut global variable for terminating RSync
rsync_request_terminate = False


def check_space():
    total, used, free = shutil.disk_usage("/tmp")
    if free <= 100000000:
        return True


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
    # Ensure Wi-Fi Connect is shutdown softly
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
    # Convert system file sizes to human readable
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def rsync_run(rsync_url):
    # Download requested content via RSync
    rsync_proc = subprocess.Popen(
        ['rsync', '-azh', '--info=progress2', '--no-i-r', '--inplace',
            rsync_url,
            './storage/library'],
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    # Read the output while downloading
    for line in iter(rsync_proc.stdout.readline, ''):
        time.sleep(1)
        # Check if the device is running out of space
        if check_space() is True:
            rsync_terminate(rsync_proc)
            yield json.dumps({'status': 500, 'running': False,
                              'message': 'Out of Space'}, 500)
            break

        # Check if user has sent terminate request
        global rsync_request_terminate
        if rsync_request_terminate is True:
            rsync_terminate(rsync_proc)
            yield json.dumps({'status': 200, 'running': False,
                              'message': 'RSync terminated by user'})
            break

        # Return log content to browser
        each_line = line.split()

        if each_line:
            json_output = {
                "transferred": each_line[0],
                "percentage": each_line[1],
                "speed": each_line[2],
                "remaining_time": each_line[3],
                "comparing_files": False
                }
        else:
            json_output = {
                "comparing_files": True
                }

        yield json.dumps(json_output) + '<br/>\n'


def rsync_terminate(rsync_proc):
    # Terminate RSync upon user request
    if rsync_proc == "terminate_request":
        global rsync_request_terminate
        rsync_request_terminate = True
        return "Sent exit command to subprocess"
    try:
        try:
            rsync_request_terminate = False
            rsync_proc.terminate()
            rsync_proc.communicate(timeout=7)
        except Exception:
            print("SIGTERM failed. Killing RSync")
            rsync_proc.kill()
    except Exception as ex:
        print("RSync was already down. " + str(ex))
    return "Rsync terminated"
