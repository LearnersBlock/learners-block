import config
import NetworkManager as Pnm  # Python NetworkManager
import subprocess
from common.errors import logger
from common.errors import WifiConnectionFailed
from common.errors import WifiHotspotStartFailed
from common.errors import WifiNetworkManagerError
from common.errors import WifiNoSuitableDevice
from common.nm_dicts import get_nm_dict
from common.nm_dicts import get_hotspot_SSID
from common.processes import led
from time import sleep

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)


class wifi:
    def analyse_access_point(ap):
        security = config.type_none

        # Based on a subset of the AP_SEC flag settings
        # (https://developer.gnome.org/NetworkManager/1.2/nm-dbus-types.html#NM80211ApSecurityFlags)
        # to determine which type of security this AP uses.
        AP_SEC = Pnm.NM_802_11_AP_SEC_NONE
        if ap.Flags & Pnm.NM_802_11_AP_FLAGS_PRIVACY and \
                ap.WpaFlags == AP_SEC and \
                ap.RsnFlags == AP_SEC:
            security = config.type_wep

        if ap.WpaFlags != AP_SEC:
            security = config.type_wpa

        if ap.RsnFlags != AP_SEC:
            security = config.type_wpa2

        if ap.WpaFlags & \
            Pnm.NM_802_11_AP_SEC_KEY_MGMT_802_1X or \
                ap.RsnFlags & \
                Pnm.NM_802_11_AP_SEC_KEY_MGMT_802_1X:
            security = config.type_enterprise

        entry = {"ssid": ap.Ssid,
                 "conn_type": security,
                 "strength": int(ap.Strength)}

        return entry

    # Returns True when a connection to a router is made, or Hotspot is live
    def check_device_state():
        # Save the wi-fi device object to a variable
        if wifi.get_device().State == Pnm.NM_DEVICE_STATE_ACTIVATED:
            return True
        else:
            return False

    def forget_all():
        # Get a list of all connections
        connections = Pnm.Settings.ListConnections()

        for connection in connections:
            if connection.GetSettings()["connection"]["type"] \
                    == "802-11-wireless":
                # Delete the identified connection
                connection.Delete()

        return True

    def connect(conn_type=config.type_hotspot,
                ssid=None,
                username=None,
                password=None):
        # Remove any existing connection made by this app
        wifi.forget()

        # Get the correct config based on type requested
        logger.info(f"Adding connection of type {conn_type}")
        conn_dict = get_nm_dict(conn_type, ssid, username, password)

        try:
            Pnm.Settings.AddConnection(conn_dict)

            # Connect
            Pnm.NetworkManager.ActivateConnection(wifi.get_connection_id(),
                                                  wifi.get_device(),
                                                  "/")

            # If not a hotspot, log the connection SSID being attempted
            if conn_type != config.type_hotspot:
                logger.info(f"Attempting connection to {ssid}")

            # Wait for ADDRCONF(NETDEV_CHANGE): wlan0: link becomes ready
            loop_count = 0
            while not wifi.check_device_state():
                sleep(1)
                loop_count += 1
                if loop_count > 30:  # Only wait 30 seconds max
                    break

            if wifi.check_device_state():
                logger.info("Connection active.")

                # Activate the LED to indicate device is connected.
                if conn_type is not config.type_hotspot:
                    led(1)
                else:
                    led(0)

                return True
            # If the current attempt is not already a hotspot attempt
            elif conn_type != config.type_hotspot:
                # Restart hotspot as connection failed
                logger.warning("Connection attempt failed.")
                wifi.connect()
            else:
                raise WifiHotspotStartFailed
        except Exception:
            logger.exception("Connection failed.")
            # If the current attempt is not already a hotspot attempt
            if conn_type == config.type_hotspot:
                raise WifiHotspotStartFailed
            else:
                wifi.connect()  # Restart hotspot as connection failed
                raise WifiConnectionFailed

    def forget(create_new_hotspot=False, all_networks=False):
        # Find and delete the hotspot connection
        try:
            if all_networks:
                for connection in Pnm.Settings.ListConnections():
                    if connection.GetSettings()["connection"]["type"] \
                            == "802-11-wireless":
                        # Delete the identified connection
                        network_id = \
                            connection.GetSettings()["connection"]["id"]
                        # Add short delay to ensure the endpoint has returned a
                        # response before disconnecting the user.
                        sleep(0.5)
                        connection.Delete()
                        logger.debug(f"Deleted connection: {network_id}")
            else:
                connection_id = wifi.get_connection_id()
                # connection_id returns false if it is missing. This can be
                # ignored as this function is often called as a precautionary
                # clean up
                if connection_id:
                    # Add short delay to ensure the endpoint has returned a
                    # response before disconnecting the user.
                    sleep(0.5)
                    connection_id.Delete()
                    logger.debug(f"Deleted connection: {config.ap_name}")

            # Disable LED indicating Wi-Fi is not active.
            led(0)

            # If requested, create new Hotspot
            if create_new_hotspot:
                wifi.refresh_networks()
                wifi.connect()

        except Exception:
            logger.exception("Failed to delete network.")
            raise WifiNetworkManagerError

        return True

    def get_connection_id():
        connection = dict([(x.GetSettings()['connection']['id'], x)
                          for x in Pnm.Settings.ListConnections()])

        if config.ap_name in connection:
            return connection[config.ap_name]
        else:
            return False

    def get_device():
        # Fetch last Wi-Fi interface found
        devices = dict([(x.DeviceType, x)
                       for x in Pnm.NetworkManager.GetDevices()])

        if Pnm.NM_DEVICE_TYPE_WIFI in devices:
            return devices[Pnm.NM_DEVICE_TYPE_WIFI]
        else:
            logger.error("No suitable or available device found.")
            raise WifiNoSuitableDevice

    def list_access_points():
        # Run IW to reduce chance of empty SSID list. Storing result
        # to return so that if IW does not work on this device the refresh
        # button will be disabled.
        iw_status = wifi.refresh_networks(retries=1)

        logger.debug('Fetching Wi-Fi networks.')

        try:
            # For each wi-fi connection in range, identify it's details
            compiled_ssids = [wifi.analyse_access_point(ap)
                              for ap in wifi.get_device().GetAccessPoints()]
        except Exception:
            logger.exception('Failed listing access points.')
            raise WifiNetworkManagerError

        # Sort SSIDs by signal strength
        compiled_ssids = sorted(compiled_ssids,
                                key=lambda x: x['strength'],
                                reverse=True)

        # Remove duplicates and own hotspot from list.
        tmp = []
        ssids = []
        for item in compiled_ssids:
            if item['ssid'] not in tmp and item['ssid'] != get_hotspot_SSID:
                ssids.append(item)
            tmp.append(item['ssid'])

        logger.debug('Finished fetching Wi-Fi networks.')

        # Return a list of available SSIDs and their security type,
        # or [] for none available.
        return ssids, iw_status

    def refresh_networks(retries=5):
        # Refreshing networks list using IW which has proven
        # to be better at refreshing than nmcli. Some devices
        # do not support this feature while the AP is active
        # and therefore returns a boolean with status of request.

        # After forget has run, NetworkManager takes a while to release
        # the Wi-Fi for iw to use it, hence the retries.
        max_runs = retries
        run = 0
        while run < max_runs:
            try:
                sleep(3)
                subprocess.check_output(["iw", "dev", "wlan0", "scan"])
            except subprocess.CalledProcessError:
                logger.warning('IW resource busy. Retrying...')
                continue
            except Exception:
                logger.error('Unknown error calling IW.')
                return False
            else:
                logger.debug('IW succeeded.')
                return True
            finally:
                run += 1

        logger.warning("IW is not accessible. This can happen on some devices "
                       "and is usually nothing to worry about.")
        return False
