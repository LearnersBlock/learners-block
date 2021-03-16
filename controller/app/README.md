# Learner's Block Controller

## Install the dependencies

Create and activate a [virtual enviroment](https://docs.python.org/3/tutorial/venv.html) based on the version of Python currently set in the `controller/Dockerfile.template`

Install the required dependencies for development mode:

`pip install -r requirements-dev.txt`

## .env file
When running the Controller outside of our Docker development enviroment, a .env file is utilised. The default settings should be fine for most cases, but a brief description of each setting is provided here:

```
# Redundent in development enviroment but required to start
DEFAULT_SSID=Learners-Block

# Redundent in development enviroment but required to start
DEFAULT_HOSTNAME=lb  

# Set the Python enviroment to development/debug
FLASK_ENV=development  

# Specify the name of the main Python script for Flask Migrate support
FLASK_APP=run  
```

## Start the Controller in development mode
`python3 run.py`
