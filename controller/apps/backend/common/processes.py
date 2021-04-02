from flask_restful import abort
import http.client as httplib
import inspect
import json
import os
import requests
import shutil
import subprocess
import time

# Set defalut global variable for terminating RSync
rsync_request_terminate = False


def check_space():
    _, _, free = shutil.disk_usage("/tmp")
    if free <= 100000000:
        return True
    return False


def check_internet():
    conn = httplib.HTTPConnection("8.8.8.8", timeout=2)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except Exception:
        conn.close()
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
                  f'{inspect.stack()[0][3] + " - " + str(ex)}.'
                  f'Retry {str(retry)}.')

            if retry == supervisor_retries:
                abort(408, status=408,
                      message=inspect.stack()[0][3] + " - " + str(ex).rstrip())

            time.sleep(2)
            retry = retry + 1

    return {'status': 200, 'message': 'Supervisor up'}, 200


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
        print("Curl request timed out. " + inspect.stack()[0][3] + " - "
              + str(ex))
        abort(408, status=408,
              message=inspect.stack()[0][3] + " - " + str(ex).rstrip())

    try:
        response.json()
    except Exception:
        return {"status_code": response.status_code, "text": response.text}

    return {"status_code": response.status_code, "text": response.text,
            "json_response": response.json()}


def database_recover():
    # Adding delay to allow user intervetion to abort
    print("Database error detected. Waiting 30 seconds before deleting "
          "database and restarting.")
    time.sleep(60)

    # Remove the .db file. It will be rebuilt fresh on next boot.
    # While this is a drastic step, it ensures devices do not
    # get bricked in the field.
    try:
        os.remove(os.path.realpath('.') + "/db/sqlite.db")
    except Exception:
        print("Failed to delete the database file. May be missing.")


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
            os.path.realpath('.') + '/storage/library/'],
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    # Read the output while downloading
    for line in iter(rsync_proc.stdout.readline, ''):
        time.sleep(1)
        # Check if the device is running out of space
        if check_space() is True:
            rsync_terminate(rsync_proc)
            yield json.dumps({"status": 500, "running": False,
                              "message": "Out of Space"})
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
        except Exception as ex:
            print("SIGTERM failed. Killing RSync" + str(ex))
            rsync_proc.kill()
    except Exception as ex:
        print("RSync was already down. " + inspect.stack()[0][3] + " - "
              + str(ex))
    return "Rsync terminated"
