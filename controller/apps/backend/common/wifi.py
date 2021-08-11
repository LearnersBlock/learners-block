from common.models import User
from dbus.mainloop.glib import DBusGMainLoop
from flask_restful import abort
from resources.errors import print_message
from run import app
import NetworkManager
import os
import subprocess
import time
import requests
import sys

DBusGMainLoop(set_as_default=True)


def handle_exit(*args):
    # Ensure Wi-Fi Connect is shutdown softly
    global wifi_process
    try:
        if 'wifi_process' in globals():
            wifi_process.terminate()
            wifi_process.communicate(timeout=8)
            sys.exit(0)
    except Exception as ex:
        print_message('handle_exit', 'Failed to terminate wifi-connect. '
                      'Executing kill.', ex)
        wifi_process.kill()
        sys.exit(0)

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

        # Wait so user gets return code before being disconnected
        # from the device
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
            print_message('wifi_connect.forget',
                          'Failed to delete connection, '
                          'trying to clear all saved connections.')
            wifi().forget_all()
            return

        # Wait before trying to launch wifi-connect
        wifi_connect().start(wait=2)

        return {'status': 200, 'message': 'ok'}

    def forget_all(self):
        # Wait so user gets return code before being disconnected
        # from the device
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

        return {'status': 200, 'message': 'ok'}


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
        except Exception as ex:
            print_message('wifi_connect.start', 'Failed to set hostname. '
                          'Setting a default instead.', ex)
            current_hostname = os.environ['DEFAULT_HOSTNAME']

        # Check the current hostname variable is not empty, and set if it is
        try:
            current_hostname
        except Exception as ex:
            print_message('wifi_connect.start', 'Error getting hostname. '
                          'Setting a default instead.', ex)
            current_hostname = os.environ['DEFAULT_HOSTNAME']

        try:
            # Refresh networks list before launch
            subprocess.run(
                ["iw", "wlan0", "scan"],
                capture_output=True,
                text=True).stdout.rstrip()
        except Exception as ex:
            print_message('wifi_connect.start', 'Error refreshing '
                          'network points.', ex)

        # Check if default SSID
        if current_hostname == os.environ['DEFAULT_HOSTNAME']:
            current_hostname = os.environ["DEFAULT_SSID"]

        # Fetch the wi-fi password
        with app.app_context():
            lb_database = User.query.filter_by(username='lb').first()

        # Start wifi connect
        if lb_database.wifi_password:
            cmd = (f'/app/common/wifi-connect/wifi-connect '
                   f'-p {lb_database.wifi_password} '
                   f'-s {current_hostname} -o 8080 --ui-directory '
                   f'/app/common/wifi-connect/ui'.split())
        else:
            cmd = (f'/app/common/wifi-connect/wifi-connect '
                   f'-s {current_hostname} -o 8080 --ui-directory '
                   f'/app/common/wifi-connect/ui'.split())

        wifi_process = subprocess.Popen(cmd)
        time.sleep(4)

        if wifi_process.poll() is not None:
            print_message('wifi_connect', 'Wifi-Connect launch failure',
                          wifi_process.returncode)
            abort(408, status=wifi_process.returncode,
                  message='Wifi-Connect launch failure')

        return {'status': 200, 'message': 'success'}

    def stop(self):
        global wifi_process

        try:
            wifi_poll = wifi_process.poll()
        except Exception as ex:
            print_message('wifi_connect.stop', 'Wifi-connect not started', ex)
            return

        if wifi_poll is not None:
            print_message('wifi_connect.stop', 'Wifi-Connect already stopped')
            return

        try:
            wifi_process.terminate()
            wifi_process.communicate(timeout=10)
        except Exception:
            # If it hasn't stopped in 10 seconds kill it
            wifi_process.kill()

    def status(self):
        global wifi_process

        try:
            curl_wifi = requests.get('http://192.168.42.1:8080', timeout=5)
            if curl_wifi.status_code == 200:
                curl_wifi = True
            else:
                curl_wifi = False
        except Exception as ex:
            print_message('wifi_connect.status', 'curl failure', ex)
            curl_wifi = False

        try:
            wifi_poll = wifi_process.poll()
        except Exception:
            wifi_poll = False

        if curl_wifi is True and wifi_poll is None:
            return 0

        elif curl_wifi is False and wifi_poll is not None:
            return 1

        abort(500, status=500,
              message='Failed on wifi-connect check')
