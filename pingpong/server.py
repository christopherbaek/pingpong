import logging
import socket
import time


# logging
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger('server')
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(CONSOLE_HANDLER)


class PingPongServer(object):

    SERVER_PORT = 9999
    SERVER_SOCKET_BACKLOG = 5
    CLIENT_SOCKET_TIMEOUT_SECONDS = 5
    SERVER_RECEIVE_BUFFER_SIZE = 1024

    def __init__(self):
        self._server_socket = None
        self._client_socket = None
        self._running = True

    def initialize(self):
        LOGGER.info('initializing')

        # create the server socket
        self._server_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM)

        # server socket parameters
        hostname = socket.gethostname()
        port = PingPongServer.SERVER_PORT

        # bind to the hostname:port
        self._server_socket.bind((hostname, port))

        # set up server socket to listen
        self._server_socket.listen(PingPongServer.SERVER_SOCKET_BACKLOG)

        LOGGER.info('initialization complete')

    def run(self):
        LOGGER.info('starting')

        while self._running:

            # wait for client connection if client not connected
            if self._client_is_disconnected():
                self._wait_for_client_connection()

            # attempt to read client message
            LOGGER.info('waiting for client message')

            try:
                client_message = self._client_socket.recv(PingPongServer.SERVER_RECEIVE_BUFFER_SIZE)
            except socket.timeout:
                LOGGER.info('timed out waiting for client message')
                self._clear_client_socket()
                break

            if client_message == '':
                LOGGER.info('detected client disconnect')
                self._clear_client_socket()
                break

            if client_message == 'ping':
                LOGGER.info('received ping message')

                # attempt to send pong
                message = 'pong ({})'.format(time.time())

                LOGGER.info('sending message: {}', message)

                try:
                    self._client_socket.send(message)
                except IOError:
                    self._clear_client_socket()

    def _client_is_disconnected(self):
        return self._client_socket is None

    def _wait_for_client_connection(self):
        LOGGER.info('waiting for client connection')

        (client_socket, client_address) = self._server_socket.accept()
        client_socket.settimeout(PingPongServer.CLIENT_SOCKET_TIMEOUT_SECONDS)
        self._client_socket = client_socket

    def _clear_client_socket(self):
        self._client_socket = None


def main():

    ping_pong_server = PingPongServer()
    ping_pong_server.initialize()
    ping_pong_server.run()


if __name__ == '__main__':
    main()
