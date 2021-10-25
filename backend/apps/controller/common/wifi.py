from common.errors import print_message
from common.models import User
from run import app
import config
import os
import subprocess
import time
import uuid


if os.environ['FLASK_ENV'].lower() == "production":
    from dbus.mainloop.glib import DBusGMainLoop
    import NetworkManager
    DBusGMainLoop(set_as_default=True)


class wifi:
    def check_connection():
        try:
            run = subprocess.run(["iw", "dev", "wlan0", "link"],
                                 capture_output=True,
                                 text=True).stdout.rstrip()
        except Exception as ex:
            print_message("check_connection", "Failed checking connection. "
                          "Returning False.", ex)
            return False

        if run.lower()[:13] == "not connected":
            return False
        else:
            return True

    def connect_to_AP(conn_type=None,
                      ssid=None,
                      username=None,
                      password=None,
                      conn_name=config.ap_name):

        if conn_type is None or ssid is None:
            print_message('connect_to_AP', 'Missing arg conn_type.')
            return False

        # Remove existing HOTSPOT if it exists and set vars for new hotspot
        if conn_type == config.type_hotspot:
            conn_name = config.hotspot_name
            wifi.forget(conn_name=config.hotspot_name)

        try:
            # Hotspot for user to connect to device
            hotspot_dict = {
                '802-11-wireless': {'band': 'bg',
                                    'mode': 'ap',
                                    'ssid': ssid},
                'connection': {'autoconnect': False,
                               'id': conn_name,
                               'interface-name': 'wlan0',
                               'type': '802-11-wireless',
                               'uuid': str(uuid.uuid4())},
                'ipv4': {'address-data':
                         [{'address': '192.168.42.1', 'prefix': 24}],
                         'addresses': [['192.168.42.1', 24, '0.0.0.0']],
                         'method': 'manual'},
                'ipv6': {'method': 'auto'}
            }

            # Include a key-mgmt string in Hotspot if setting a password
            if password:
                password_key_mgmt = {'802-11-wireless-security':
                                     {'key-mgmt': 'wpa-psk', 'psk': password}}

                hotspot_dict.update(password_key_mgmt)

            # "MIT SECURE" network.
            enterprise_dict = {
                '802-11-wireless': {'mode': 'infrastructure',
                                    'security': '802-11-wireless-security',
                                    'ssid': ssid},
                '802-11-wireless-security':
                    {'auth-alg': 'open', 'key-mgmt': 'wpa-eap'},
                '802-1x': {'eap': ['peap'],
                           'identity': username,
                           'password': password,
                           'phase2-auth': 'mschapv2'},
                'connection': {'id': conn_name,
                               'type': '802-11-wireless',
                               'uuid': str(uuid.uuid4())},
                'ipv4': {'method': 'auto'},
                'ipv6': {'method': 'auto'}
            }

            # No auth/'open' connection.
            none_dict = {
                '802-11-wireless': {'mode': 'infrastructure',
                                    'ssid': ssid},
                'connection': {'id': conn_name,
                               'type': '802-11-wireless',
                               'uuid': str(uuid.uuid4())},
                'ipv4': {'method': 'auto'},
                'ipv6': {'method': 'auto'}
            }

            # Hidden, WEP, WPA, WPA2, password required.
            passwd_dict = {
                '802-11-wireless': {'mode': 'infrastructure',
                                    'security': '802-11-wireless-security',
                                    'ssid': ssid},
                '802-11-wireless-security':
                    {'key-mgmt': 'wpa-psk', 'psk': password},
                'connection': {'id': conn_name,
                               'type': '802-11-wireless',
                               'uuid': str(uuid.uuid4())},
                'ipv4': {'method': 'auto'},
                'ipv6': {'method': 'auto'}
            }

            if conn_type == config.type_hotspot:
                conn_dict = hotspot_dict
            elif conn_type == config.type_none:
                conn_dict = none_dict
            elif (conn_type == config.type_wep or
                    conn_type == config.type_wpa or
                    conn_type == config.type_wpa2):
                conn_dict = passwd_dict
            elif conn_type == config.type_enterprise:
                conn_dict = enterprise_dict
            else:
                print_message('connect_to_AP', 'Invalid conn_type.')
                return False

            NetworkManager.Settings.AddConnection(conn_dict)
            print(f"Added connection of type {conn_type}")

            # Find this connection and its device
            connections = NetworkManager.Settings.ListConnections()
            connections = dict([(x.GetSettings()['connection']['id'], x)
                                for x in connections])
            conn = connections[conn_name]

            # Find a suitable device
            ctype = conn.GetSettings()['connection']['type']
            dtype = {'802-11-wireless': NetworkManager.NM_DEVICE_TYPE_WIFI} \
                .get(ctype, ctype)
            devices = NetworkManager.NetworkManager.GetDevices()

            for dev in devices:
                if dev.DeviceType == dtype:
                    break
            else:
                print_message('connect_to_AP', 'No suitable and '
                              f"available {ctype} device found.")
                return False

            # Connect
            NetworkManager.NetworkManager.ActivateConnection(conn, dev, "/")
            print("Activated connection.")

            # Wait for ADDRCONF(NETDEV_CHANGE): wlan0: link becomes ready
            print('Waiting for connection to become active...')
            loop_count = 0
            while dev.State != NetworkManager.NM_DEVICE_STATE_ACTIVATED:
                time.sleep(1)
                loop_count += 1
                if loop_count > 30:  # only wait 30 seconds max
                    break

            if dev.State == NetworkManager.NM_DEVICE_STATE_ACTIVATED:
                print('Connection is live.')
                return True

        except Exception as ex:
            print_message('connect_to_AP', 'Connection failed.', ex)

        print_message('connect_to_AP', 'Connection failed.')
        return False

    def forget(conn_name=config.ap_name):
        # Find and delete the hotspot connection
        try:
            connections = NetworkManager.Settings.ListConnections()
            connections = dict([(x.GetSettings()['connection']['id'], x)
                                for x in connections])

            if conn_name in connections:
                conn = connections[conn_name]
                conn.Delete()

        except Exception as ex:
            print_message('wifi.forget', 'Failed to delete network. '
                          'Trying reset all.', ex)
            time.sleep(5)  # Delay to allow time for error to resolve
            wifi.forget_all()

        # If a hotspot is needed then start it
        if conn_name == config.ap_name:
            # Ensure NetworkManager is ready before starting new hotspot
            time.sleep(5)

            wifi.start_hotspot()
        return True

    def forget_all():
        # Get a list of all connections
        connections = NetworkManager.Settings.ListConnections()

        for connection in connections:
            if connection.GetSettings()["connection"]["type"] \
                    == "802-11-wireless":
                # Delete the identified connection
                connection.Delete()

        # Launch wifi hotspot
        wifi.start_hotspot()

        return True

    # Get user defined hotspot password.
    def get_hotspot_password():
        with app.app_context():
            lb_database = User.query.filter_by(username='lb').first()
        return lb_database.wifi_password

    # Get user specified hotspot SSID.
    def get_hotspot_SSID():
        # Get the current hostname of the container, and
        # set a default on failure
        try:
            current_hostname = subprocess.run(["hostname"],
                                              capture_output=True,
                                              text=True).stdout.rstrip()
        except Exception as ex:
            print_message('wifi.get_hotspot_SSID', 'Failed to get hostname. '
                          'Setting a default instead.', ex)
            current_hostname = config.default_hostname

        # If default hostname is active then provide default SSID
        if current_hostname == config.default_hostname:
            return config.default_ssid
        # Otherwise return the hostname to use as an SSID
        else:
            return current_hostname

    # Return a list of available SSIDs and their security type,
    # or [] for none available or error.
    def list_access_points():
        # Run IW to reduce chance of empty SSID list
        refresh_status = wifi.refresh_networks()

        # Fetch current hotspot name
        currentSSID = wifi.get_hotspot_SSID()

        ssids = []  # list to be returned

        for dev in NetworkManager.NetworkManager.GetDevices():
            if dev.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:
                continue
            for ap in dev.GetAccessPoints():
                security = config.type_none

                # Based on a subset of the AP_SEC flag settings
                # (https://developer.gnome.org/NetworkManager/1.2/nm-dbus-types.html#NM80211ApSecurityFlags)
                # determine which type of security this AP uses.
                AP_SEC = NetworkManager.NM_802_11_AP_SEC_NONE
                if ap.Flags & NetworkManager.NM_802_11_AP_FLAGS_PRIVACY and \
                        ap.WpaFlags == AP_SEC and \
                        ap.RsnFlags == AP_SEC:
                    security = config.type_wep

                if ap.WpaFlags != AP_SEC:
                    security = config.type_wpa

                if ap.RsnFlags != AP_SEC:
                    security = config.type_wpa2

                if ap.WpaFlags & \
                    NetworkManager.NM_802_11_AP_SEC_KEY_MGMT_802_1X or \
                        ap.RsnFlags & \
                        NetworkManager.NM_802_11_AP_SEC_KEY_MGMT_802_1X:
                    security = config.type_enterprise

                entry = {"ssid": ap.Ssid,
                         "security": security,
                         "strength": int(ap.Strength)}

                # Do not add duplicates to the list
                if ssids.__contains__(entry):
                    continue

                # Do not add own hotspot to the list
                if ap.Ssid == currentSSID:
                    continue

                ssids.append(entry)

        return ssids, refresh_status

    def refresh_networks():
        try:
            # Refresh networks list using IW which has proven
            # to be better at refreshing than nmcli. Some devices
            # do not support this feature while the AP is active
            # and therefore returns a boolean with status of request
            subprocess.check_output(
                ["iw", "dev", "wlan0", "scan"])
            return True
        except subprocess.CalledProcessError as ex:
            print_message('wifi.refresh_networks',
                          'Error refreshing '
                          'network points.', ex)
            return False

    def start_hotspot():
        # On some devices, fetching available wifi networks in the area is only
        # possible before the hotspot is started and therefore called here.
        try:
            wifi.refresh_networks()
        except Exception as ex:
            print_message('wifi.start_hotspot', 'Error refreshing '
                          'network points. Starting hotspot anyway', ex)

        return wifi.connect_to_AP(conn_type=config.type_hotspot,
                                  ssid=wifi.get_hotspot_SSID(),
                                  username=None,
                                  password=wifi.get_hotspot_password())
