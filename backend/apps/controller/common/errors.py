import config
import logging

# Create custom logger
syslog = logging.StreamHandler()
logger = logging.getLogger('syslog')
logger.addHandler(syslog)
formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - [%(module)s:'
                              '%(lineno)d] - %(message)s', "%Y-%m-%d %H:%M:%S")
syslog.setFormatter(formatter)
logger.setLevel(logging.WARNING)
logger.propagate = False

# Change default logging mode when in development environmnets
if config.dev_mode or config.dev_device:
    logger.setLevel(logging.DEBUG)


# Error classes for Flask-Restful
class AppStoreFetchFailed(Exception):
    pass


class DockerContainerException(Exception):
    pass


class DockerException(Exception):
    pass


class DockerImageNotFound(Exception):
    pass


class DockerImageStatus(Exception):
    pass


class DockerSocket(Exception):
    pass


class FileManagerExtractFail(Exception):
    pass


class FileManagerInvalidString(Exception):
    pass


class SupervisorCurlFailed(Exception):
    pass


class SupervisorUnreachable(Exception):
    pass


class WifiConnectionFailed(Exception):
    pass


class WifiDeviceNotFound(Exception):
    pass


class WifiHotspotStartFailed(Exception):
    pass


class WifiInvalidConnectionType(Exception):
    pass


class WifiNetworkManagerError(Exception):
    pass


class WifiNoSuitableDevice(Exception):
    pass


# Custom error messages for Flask-RESTful to return
errors = {
    "AppStoreFetchFailed": {
        "message": "Failed fetching app list from Git.",
        "status": 408
    },
    "DockerContainerException": {
         "message": "Container exited with non-zero code.",
         "status": 500
     },
    "DockerException": {
         "message": "A Docker command has failed.",
         "status": 500
     },
    "DockerImageStatus": {
         "message": "Failed getting Docker image status.",
         "status": 500
     },
    "DockerImageNotFound": {
         "message": "Docker image could not be found.",
         "status": 500
     },
    "DockerSocket": {
         "message": "Docker UNIX socket is unreachable.",
         "status": 502
     },
    "FileManagerExtractFail": {
         "message": "Failed to extract archive.",
         "status": 500
     },
    "FileManagerInvalidString": {
         "message": "An invalid string was passed to File Manager.",
         "status": 500
     },
    "SupervisorCurlFailed": {
         "message": "Failure while communicating with Balena Supervisor.",
         "status": 408
     },
    "SupervisorUnreachable": {
         "message": "Balena Supervisor could not be reached.",
         "status": 408
     },
    "WifiConnectionFailed": {
         "message": "System error while establishing Wi-Fi connection.",
         "status": 500
     },
    "WifiDeviceNotFound": {
         "message": "Requested device not available.",
         "status": 500
     },
    "WifiHotspotStartFailed": {
         "message": "System error starting hotspot.",
         "status": 500
     },
    "WifiInvalidConnectionType": {
         "message": "Invalid connection type.",
         "status": 500
     },
    "WifiNetworkManagerError": {
         "message": "Failed communicating with Network Manager.",
         "status": 500
     },
    "WifiNoSuitableDevice": {
         "message": "No suitable Wi-Fi device available.",
         "status": 404
     }
}
