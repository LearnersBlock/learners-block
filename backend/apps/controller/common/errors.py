import config
import logging

# Create custom logger
logger = logging.getLogger('syslog')
syslog = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - [%(module)s:'
                              '%(lineno)d] - %(message)s', "%Y-%m-%d %H:%M:%S")
syslog.setFormatter(formatter)
logger.addHandler(syslog)
logger.setLevel(logging.WARNING)

# Change default logging mode when in development environmnets
if config.dev_mode:
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


class WifiApFail(Exception):
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
    "WifiApFail": {
         "message": "Failed to activate Wi-Fi",
         "status": 500
     }
}
