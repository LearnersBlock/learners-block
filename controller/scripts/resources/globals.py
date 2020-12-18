import os

# Set default version variables
LB_VER = 0
FRONTEND_VER = 0
BACKEND_VER = 0
CONTROLLER_VER = 0
FILE_MANAGER_VER = 0
WIFICONNECT_UI_VER = 0

try:
    # Import balena device info
    BALENA_SUPERVISOR_API_KEY = os.environ['BALENA_SUPERVISOR_API_KEY']
    BALENA_SUPERVISOR_ADDRESS = os.environ['BALENA_SUPERVISOR_ADDRESS']
    BALENA_DEVICE_UUID = os.environ['BALENA_DEVICE_UUID']
    BALENA_APP_ID = os.environ['BALENA_APP_ID']

    # Import software version numbers
    LB_VER = os.environ['LB_VER']
    FRONTEND_VER = os.environ['FRONTEND_VER']
    BACKEND_VER = os.environ['BACKEND_VER']
    CONTROLLER_VER = os.environ['CONTROLLER_VER']
    FILE_MANAGER_VER = os.environ['FILE_MANAGER_VER']
    WIFICONNECT_UI_VER = os.environ['WIFICONNECT_UI_VER']

except Exception as ex:
    print("Failed to fetch all the variables. Continuing without but errors wil likely occur. " + str(ex))
