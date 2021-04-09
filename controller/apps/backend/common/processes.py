from flask_restful import abort
import inspect
import os
import requests
import shutil
import socket
import subprocess
import time


# Set global variables
download_log = ''
download_terminate = 0
rsync_log = ''
rsync_status = {
    "progress": 'loading'
    }


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
        print(ex, flush=True)
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
    print("Database error detected. Waiting 60 seconds before deleting "
          "database and restarting.")
    time.sleep(60)

    # Remove the .db file. It will be rebuilt fresh on next boot.
    # While this is a drastic step, it ensures devices do not
    # get bricked in the field.
    try:
        os.remove(os.path.realpath('.') + "/db/sqlite.db")
    except Exception:
        print("Failed to delete the database file. May be missing.")


def download_start(url: str):
    global download_log
    global download_terminate
    download_log = 0
    downloaded_percentage = 0
    try:
        resp = requests.get(url, stream=True)
    except Exception:
        download_log = "error"
        return
    total = int(resp.headers.get('content-length', 0))
    with open(os.path.realpath('.') + '/storage/library/' + url.split('/')[-1], 'wb') as file:
        for data in resp.iter_content(chunk_size=1024):
            if download_terminate == 1:
                download_terminate = 0
                return {"progress": "termianted"}
            size = file.write(data)
            downloaded_percentage += size
            download_log = downloaded_percentage/total*100/100

    print("Download complete")


def download_get_status():
    global download_log
    if check_space() is True:
        download_terminate()
        return {"progress": "space-error"}
    return {"progress": download_log}


def download_terminate():
    # Terminate RSync upon user request
    global download_terminate
    download_terminate = 1


def human_size(nbytes):
    # Convert system file sizes to human readable
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])


def rsync_start(rsync_url):
    global rsync_proc
    global rsync_status
    rsync_status = {
            "progress": 'loading'
            }

    try:
        if rsync_proc.poll() is None:
            return "running"
    except Exception:
        pass

    print("Starting Download")
    rsync_proc = subprocess.Popen(
        ['rsync', '-azh', '--info=progress2', '--no-i-r', '--inplace',
            rsync_url,
            os.path.realpath('.') + '/storage/library/'],
        stdout=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1,
        start_new_session=True
    )

    time.sleep(4)

    if rsync_proc.poll() is not None and rsync_proc.returncode != 0:
        rsync_terminate(outcome='error')
        return 1

    try:
        for line in rsync_proc.stdout:
            global rsync_log
            rsync_log = line
    except Exception:
        print("RSync Proc terminated. Ending logging")

    rsync_terminate(outcome="complete")

    return 0


def rsync_get_status():
    global rsync_status
    global rsync_log

    if check_space() is True:
        rsync_terminate(outcome='space-error')
        return {"progress": "space-error"}

    if rsync_status['progress'] == "error":
        return {"progress": rsync_status['progress']}

    if rsync_status['progress'] == "complete":
        return {"progress": rsync_status['progress']}

    # Split log lines
    each_line = rsync_log.split()

    if each_line:
        print(each_line[1][:-1])
        json_output = {
            "progress": int(each_line[1][:-1])/100,
            "transferred": each_line[0],
            "speed": each_line[2],
            "remaining_time": each_line[3]
            }
    else:
        json_output = {
            "progress": 'checking-files',
            "transferred": 0,
            "speed": 0,
            "remaining_time": 0
            }

    return json_output


def rsync_terminate(outcome='complete'):
    # Terminate RSync upon user request
    try:
        global rsync_proc
        rsync_proc.terminate()
        rsync_proc.communicate(timeout=5)
        rsync_proc.wait(timeout=None)
        subprocess.run(["killall", "-r", "rsync"])
        print("Terminated RSync")
    except Exception as ex:
        print("SIGTERM failed. Killing RSync" + str(ex))
        try:
            rsync_proc.kill()
        except Exception:
            print("Could not kill")

    global rsync_log
    rsync_log = ''

    global rsync_status
    rsync_status = {
                "progress": outcome
                }
    return "Rsync terminated"
