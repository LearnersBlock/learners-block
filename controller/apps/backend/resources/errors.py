def print_message(function='None', message='None', ex='None'):
    print('function: ' + str(function) + " - message: " +
          str(message) + " - error: " + str(ex), flush=True)


errors = {
    "DatabaseError": {
        "message": "Error accessing the SQLite Database",
        "status": 500
    }
}
