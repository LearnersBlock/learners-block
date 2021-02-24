from flask_restful import abort
import resources.config
import resources.globals
import NetworkManager
import requests
import time
import subprocess
import sys

def check_supervisor(supervisor_retries, timeout):
    # Check Balena Supervisor is ready
    retry = 1

    while True:
        try:
            supervisor_status = requests.get(
                f'{resources.globals.BALENA_SUPERVISOR_ADDRESS}/ping',
                headers={"Content-Type": "application/json"}, timeout=timeout
            )

            if supervisor_status.status_code == 200:
                break
            else:
                abort(supervisor_status.status_code,
                      status=supervisor_status.status_code,
                      message='Supervisor returned error code.')

        except Exception as ex:
            print(f'Waiting for Balena Supervisor to be ready. {str(ex)}. Retry {str(retry)}.')

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
                f'{resources.globals.BALENA_SUPERVISOR_ADDRESS}{cmd["path"]}{resources.globals.BALENA_SUPERVISOR_API_KEY}',
                json=[cmd["string"]],
                headers={"Content-Type": "application/json"}, timeout=timeout
            )

        elif cmd["method"] == 'post-data':
            response = requests.post(
                f'{resources.globals.BALENA_SUPERVISOR_ADDRESS}{cmd["path"]}{resources.globals.BALENA_SUPERVISOR_API_KEY}',
                data=cmd["string"],
                headers={"Content-Type": "application/json"}, timeout=timeout
            )

        elif cmd["method"] == 'patch':

            response = requests.patch(
                f'{resources.globals.BALENA_SUPERVISOR_ADDRESS}{cmd["path"]}{resources.globals.BALENA_SUPERVISOR_API_KEY}',
                data=cmd["string"],
                headers={"Content-Type": "application/json"}, timeout=timeout
            )

        elif cmd["method"] == 'get':

            response = requests.get(
                f'{resources.globals.BALENA_SUPERVISOR_ADDRESS}{cmd["path"]}{resources.globals.BALENA_SUPERVISOR_API_KEY}',
                headers={"Content-Type": "application/json"}, timeout=timeout
            )
    except Exception as ex:
        print("Curl request timed out. " + str(ex))
        abort(408, status=408,
              message=str(ex).rstrip())

    try:
        response.json()
    except Exception:
        return {"status_code": response.status_code, "text": response.text}

    return {"status_code": response.status_code, "text": response.text, "json_response": response.json()}

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

class container:
    def status(self, container, sleep=0.1):
        time.sleep(sleep)
        response = curl(method="get",
                        path="/v2/state/status?apikey=")

        for entry in response["json_response"]["containers"]:
            if entry['serviceName'] == container:
                return response, entry
 
        abort(404, status=404,
            message='Container not found')

    def start(self, container, sleep=0.1):
        time.sleep(sleep)
        response = curl(method="post-data",
                        path=f"/v2/applications/{resources.globals.BALENA_APP_ID}/start-service?apikey=",
                        string='{"serviceName": "%s"}' % (container))

        return response

    def stop(self, container, sleep=0.1):
        time.sleep(sleep)
        response = curl(method="post-data",
                        path=f"/v2/applications/{resources.globals.BALENA_APP_ID}/stop-service?apikey=",
                        string='{"serviceName": "%s"}' % (container))

        print(str(response["text"]) + str(response["status_code"]))
        return response


class wifi:
    def check_connection(self):

        run = subprocess.run(["iwgetid", "-r"], capture_output=True, text=True).stdout.rstrip()

        return run

    def forget(self):
        status = 1

        # Wait so user gets return code before disconnecting
        time.sleep(5)

        wifi_connect().stop()

        # Get the name of the current wifi network
        current_ssid = wifi().check_connection()

        # Get a list of all connections
        connections = NetworkManager.Settings.ListConnections()

        for connection in connections:
            if connection.GetSettings()["connection"]["type"] == "802-11-wireless":
                if connection.GetSettings()["802-11-wireless"]["ssid"] == current_ssid:
                    print("wifi_forget: Deleting connection "
                          + connection.GetSettings()["connection"]["id"])

                    # Delete the identified connection and change status code to 0 (success)
                    connection.Delete()
                    status = 0

        # Check that a connection was deleted
        if status == 1:
            print('Failed to delete connection, trying to clear all saved connections.')
            wifi().forget_all()
            return {'status': 500, 'message': 'wifi_forget failed, attempted wifi_forget_all instead'}, 500

        # Wait before trying to launch wifi-connect
        wifi_connect().start(wait=2)

        print('Success, connection deleted.')
        return {'status': 200, 'message': 'ok'}, 200

    def forget_all(self):
        # Wait so user gets return code before disconnecting
        time.sleep(5)

        wifi_connect().stop()

        # Get a list of all connections
        connections = NetworkManager.Settings.ListConnections()

        for connection in connections:
            if connection.GetSettings()["connection"]["type"] == "802-11-wireless":
                print("Deleting connection "
                      + connection.GetSettings()["connection"]["id"])

                # Delete the identified connection and change status code to 200 (success)
                connection.Delete()

        # Wait before trying to launch wifi-connect
        wifi_connect().start(wait=2)

        print('Success, all wi-fi connections deleted, wifi-connect started.')
        return {'status': 200, 'message': 'ok'}, 200


class wifi_connect:
    def start(self, wait=0.1):

        global wifi_process

        time.sleep(wait)

        # Check default hostname variables is not empty, and set if it is
        try:
            resources.config.default_hostname
        except Exception:
            resources.config.default_hostname = 'lb'

        # Get the current hostname of the container, and set a default on failure
        try:
            current_hostname = subprocess.run(["hostname"], capture_output=True, text=True).stdout.rstrip()
        except Exception:
            current_hostname = resources.config.default_hostname

        # Check the current hostname variable is not empty, and set if it is
        try:
            current_hostname
        except Exception:
            current_hostname = resources.config.default_hostname

        # Decide whether to use default SSID or match hostname
        if current_hostname == resources.config.default_hostname:
            cmd = f'/app/common/wifi-connect/wifi-connect -s {resources.config.deafult_ssid} \
                -o 8080 --ui-directory /app/common/wifi-connect/ui'.split()
        else:
            cmd = f'/app/common/wifi-connect/wifi-connect -s {current_hostname} \
                -o 8080 --ui-directory /app/common/wifi-connect/ui'.split()

        wifi_process = subprocess.Popen(cmd)
        time.sleep(4)

        if wifi_process.poll() is not None:
            print('Wifi-Connect launch failure ' + wifi_process.returncode)
            abort(408, status=wifi_process.returncode,
                  message='Wifi-Connect launch failure')

        return {'status': 200, 'message': 'success'}, 200

    def stop(self):
        global wifi_process

        try:
            wifi_poll = wifi_process.poll()
        except Exception:
            print("wifi-connect not started")
            return 1

        if wifi_poll is not None:
            print("wifi-connect already stopped")
            return 1

        try:
            wifi_process.terminate()
            wifi_process.communicate(timeout=10)
        except Exception:
            wifi_process.kill()

        return 0

    def status(self):
        global wifi_process

        try:
            curl_wifi = requests.get('http://192.168.42.1:8080', timeout=5)
            if curl_wifi.status_code == 200:
                curl_wifi = True
            else:
                curl_wifi = False
        except Exception:
            curl_wifi = False

        try:
            wifi_poll = wifi_process.poll()
        except Exception:
            wifi_poll = False

        if curl_wifi is True and wifi_poll is None:
            return 0

        elif curl_wifi is False and wifi_poll is not None:
            return 1

        return 500
