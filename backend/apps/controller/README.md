# Learner's Block Controller

## Install the dependencies

Create and activate a [virtual environment](https://docs.python.org/3/tutorial/venv.html) based on the version of Python currently set in `controller/Dockerfile.template`.

Install the required dependencies for development mode:

`pip install -r requirements-dev.txt`

## .env file
When running the Controller outside of our Docker development environment, a .env file is utilised. The default settings should be fine for most cases, but a brief description of each setting is provided here:

```
# Set the Python environment to development/debug
FLASK_ENV=development  

# Specify the name of the main Python script for Flask Migrate support
FLASK_APP=run  
```

## Start the Controller in development mode
`python3 run.py`