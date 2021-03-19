from flask_restful import abort
import inspect
import NetworkManager
import os
import subprocess
import time
import requests
import sys


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
        print("Wifi-connect was already down. " + inspect.stack()[0][3] + " - "
              + str(ex))
    print("Finshed the exit process")
    sys.exit(0)


class wifi:
    def check_connection(self):

        run = subprocess.run(["iwgetid", "-r"],
                             capture_output=True,
                             text=True).stdout.rstrip()

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
            if connection.GetSettings()["connection"]["type"] \
               == "802-11-wireless":
                if connection.GetSettings()["802-11-wireless"]["ssid"] \
                   == current_ssid:
                    print("wifi_forget: Deleting connection "
                          + connection.GetSettings()["connection"]["id"])

                    # Delete the identified connection and change status
                    # code to 0 (success)
                    connection.Delete()
                    status = 0

        # Check that a connection was deleted
        if status == 1:
            print('Failed to delete connection, '
                  'trying to clear all saved connections.')
            wifi().forget_all()
            return {'status': 500, 'message': 'wifi_forget failed, '
                    'attempted wifi_forget_all instead'}, 500

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
            if connection.GetSettings()["connection"]["type"] \
                    == "802-11-wireless":
                print("Deleting connection "
                      + connection.GetSettings()["connection"]["id"])

                # Delete the identified connection and change
                # status code to 200 (success)
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
            os.environ['DEFAULT_HOSTNAME']
        except Exception:
            os.environ['DEFAULT_HOSTNAME'] = 'lb'

        # Get the current hostname of the container, and
        # set a default on failure
        try:
            current_hostname = subprocess.run(["hostname"],
                                              capture_output=True,
                                              text=True).stdout.rstrip()
        except Exception:
            current_hostname = os.environ['DEFAULT_HOSTNAME']

        # Check the current hostname variable is not empty, and set if it is
        try:
            current_hostname
        except Exception:
            current_hostname = os.environ['DEFAULT_HOSTNAME']

        # Decide whether to use default SSID or match hostname
        if current_hostname == os.environ['DEFAULT_HOSTNAME']:
            cmd = (f'/app/common/wifi-connect/wifi-connect -s '
                   f'{os.environ["DEFAULT_SSID"]} -o 8080 '
                   f'--ui-directory /app/common/wifi-connect/ui'.split())
        else:
            cmd = (f'/app/common/wifi-connect/wifi-connect '
                   f'-s {current_hostname} -o 8080 --ui-directory '
                   f'/app/common/wifi-connect/ui'.split())

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