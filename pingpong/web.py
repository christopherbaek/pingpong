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


class RabbitMQClient(object):

    def __init__(self):
        self._credentials = pika.PlainCredentials('pingpongweb', 'pingpongweb')
        self._parameters = pika.ConnectionParameters('localhost', 5672, '/', self._credentials)
        self._connection = pika.SelectConnection(
            self._parameters,
            self._on_connection_open,
            stop_ioloop_on_close=False)
        self._channel = None
    
    def _on_connection_open(self, connection):
        self._connection.channel(on_open_callback=self._on_channel_open)
    
    def _on_channel_open(self, channel):
        self._channel = channel
        self._channel.basic_consume(self._handle_state_response, queue='state_response')

    def _handle_state_response(self, channel, method, properties, body):
        LOGGER.info('received state response')

        emit('state_response', body, json=True)

        self._channel.basic_ack(delivery_tag = method.delivery_tag)


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

    # RABBIT_MQ_CHANNEL.basic_publish(exchange='', routing_key='state_request', body='')

    # Mock state response
    state = {
        'device_connection_status': 'Connected',
        'device_id': '12345'
    }

    RABBIT_MQ_CHANNEL.basic_publish(
        exchange='',
        routing_key='state_response',
        body=json.dumps(state))


if __name__ == '__main__':
    #SOCKET_IO.run(FLASK_APP, host='0.0.0.0', port=8888)
    RABBIT_MQ_CONNECTION.ioloop.start()
