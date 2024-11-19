"""
This script runs the DormitoryManager application using a development server.
"""

from os import environ
from pickle import TRUE
from DormitoryManager import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(environ.get('SERVER_PORT', '21658'))
    except ValueError:
        PORT = 21658
    app.run(HOST, PORT, debug=True)
