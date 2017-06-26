"""
The admin web application
"""
import json
import pika

from flask import Flask, render_template
from flask_socketio import SocketIO, emit


# The Flask application
FLASK_APP = Flask(__name__)

# The Socket.IO application
SOCKET_IO = SocketIO(FLASK_APP)


@FLASK_APP.route('/')
def index():
    """
    The root route of the Flask application
    """
    return render_template(
        'index.html',
        application_name='Ping Pong Server Admin')


@SOCKET_IO.on('state_request')
def handle_state_request():
    state = {
        'device_connection_status': 'Connected',
        'device_id': '12345'
    }

    emit('state_response', json.dumps(state), json=True)


if __name__ == '__main__':
    SOCKET_IO.run(FLASK_APP, host='0.0.0.0', port=8888)

