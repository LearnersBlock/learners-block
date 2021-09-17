# Message formatter for printing standard messages from functions
def print_message(function='Unspecified', message='None', ex='Not Specified'):
    print('function: ' + str(function) + " - message: " +
          str(message) + " - error: " + str(ex), flush=True)


# Custom error messages for Flask-RESTful to return
errors = {
    "DatabaseError": {
        "message": "Error accessing the SQLite Database",
        "status": 500
    }
}
