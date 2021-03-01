import os
from dotenv import load_dotenv

# Load Python library for managing enviroment variables
load_dotenv()

# Set default version variables
VER = 0

try:
    # Import balena device info
    BALENA_SUPERVISOR_API_KEY = os.environ['BALENA_SUPERVISOR_API_KEY']
    BALENA_SUPERVISOR_ADDRESS = os.environ['BALENA_SUPERVISOR_ADDRESS']
    BALENA_DEVICE_UUID = os.environ['BALENA_DEVICE_UUID']
    BALENA_APP_ID = os.environ['BALENA_APP_ID']

    # Import software version number
    VER = os.getenv('VER')

except Exception as ex:
    print("Failed to fetch all the variables. Continuing without but \
           errors wil likely occur. " + str(ex))
