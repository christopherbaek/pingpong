"""
The admin web application
"""
import json
import logging
import pika

from flask import Flask, render_template
from flask_socketio import SocketIO, emit


# logging
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger('web')
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(CONSOLE_HANDLER)


# The Flask application
FLASK_APP = Flask(__name__)

# The Socket.IO application
SOCKET_IO = SocketIO(FLASK_APP)


@FLASK_APP.route('/')
def index():
    LOGGER.info('received index GET request')

    return render_template(
        'index.html',
        application_name='Ping Pong Server Admin')


@SOCKET_IO.on('state_request')
def handle_state_request():
    LOGGER.info('received state request')

    state = {
        'device_connection_status': 'Connected',
        'device_id': '12345'
    }

    emit('state_response', json.dumps(state), json=True)


if __name__ == '__main__':
    SOCKET_IO.run(FLASK_APP, host='0.0.0.0', port=8888)
