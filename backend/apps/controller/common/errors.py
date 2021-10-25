import logging
import os

# Create custom logger
logger = logging.getLogger('syslog')
syslog = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] - [%(levelname)s] - [%(module)s:'
                              '%(lineno)d] - %(message)s', "%Y-%m-%d %H:%M:%S")
syslog.setFormatter(formatter)
logger.addHandler(syslog)
logger.setLevel(logging.WARNING)

# Change default logging mode when in development environmnets
if "BALENA_APP_NAME" in os.environ and \
        os.environ['BALENA_APP_NAME'].lower() == "lb-dev":
    logger.setLevel(logging.DEBUG)
elif os.environ['FLASK_ENV'].lower() == "development":
    logger.setLevel(logging.DEBUG)

# Custom error messages for Flask-RESTful to return
errors = {
    "DatabaseError": {
        "message": "Error accessing the SQLite Database",
        "status": 500
    }
}
