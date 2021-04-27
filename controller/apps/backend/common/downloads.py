from common.processes import check_space
from common.processes import chown
import os
import requests
import subprocess
import time


# Set global variables
download_log = {}
download_process_running = False
download_terminated = 0
rsync_log = ''
rsync_status = {}


def download_start(url: str):
    global download_log
    global download_terminated
    global download_process_running

    if download_process_running:
        download_terminate()
        return

    download_process_running = True

    download_log = {}
    downloaded_percentage = 0
    try:
        resp = requests.get(url, stream=True, timeout=5)
    except Exception:
        download_log['progress'] = "error"
        download_process_running = False
        return

    total = int(resp.headers.get('content-length', 0))
    with open(os.path.realpath('.') + '/storage/library/' +
              url.split('/')[-1], 'wb') as file:
        for data in resp.iter_content(chunk_size=1024):
            if download_terminated == 1:
                break
            size = file.write(data)
            downloaded_percentage += size
            download_log = {
                "progress": downloaded_percentage/total*100/100,
                "MBytes": downloaded_percentage/1000000,
            }

    chown(path=os.path.realpath('.') + '/storage/library/' +
              url.split('/')[-1], owner='65534:65534')

    download_process_running = False
    print("Download complete")


def download_get_status():
    global download_log
    global download_terminated

    if download_terminated == 1:
        download_terminated = 0
        return {"progress": 1}

    if check_space() is True:
        download_terminate()
        return {"progress": "space-error"}

    return download_log


def download_terminate():
    # Terminate RSync upon user request
    global download_terminated
    download_terminated = 1


def rsync_start(rsync_url):
    global rsync_proc
    global rsync_status
    rsync_status = {
            "progress": "loading"
            }

    try:
        if rsync_proc.poll() is None:
            rsync_terminate(outcome="error")
            return 1
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

    chown(path=os.path.realpath('.') + '/storage/library/', owner='65534:65534')

    rsync_terminate(outcome="complete")

    return 0


def rsync_get_status():
    global rsync_status
    global rsync_log

    if check_space() is True:
        rsync_terminate(outcome='space-error')
        rsync_status['progress'] = "space-error"
        return rsync_status

    if rsync_status['progress'] == "error":
        return rsync_status

    if rsync_status['progress'] == "complete":
        return rsync_status

    # Split log lines
    each_line = rsync_log.split()

    if each_line:
        print(each_line[1][:-1])
        output = {
            "progress": int(each_line[1][:-1])/100,
            "transferred": each_line[0],
            "speed": each_line[2],
            "remaining_time": each_line[3]
            }
    else:
        output = {
            "progress": 'checking-files',
            "transferred": 0,
            "speed": 0,
            "remaining_time": 0
            }

    return output


def rsync_terminate(outcome='complete'):
    # Terminate RSync upon user request
    try:
        global rsync_proc
        rsync_proc.terminate()
        rsync_proc.communicate(timeout=5)
        rsync_proc.wait(timeout=None)
        subprocess.run(["killall", "-r", "rsync"])
        print("Terminated RSync")
    except Exception:
        try:
            rsync_proc.kill()
        except Exception:
            pass

    global rsync_log
    rsync_log = ''

    global rsync_status
    rsync_status['progress'] = outcome

    return "Rsync terminated"
