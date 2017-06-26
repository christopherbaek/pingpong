
import socket
import time


class PingPongServer(object):

    SERVER_PORT = 5000
    SERVER_SOCKET_BACKLOG = 5
    CLIENT_SOCKET_TIMEOUT_SECONDS = 5
    SERVER_RECEIVE_BUFFER_SIZE = 1024

    def __init__(self,
                 client_timeout_handler=None,
                 client_disconnect_handler=None,
                 client_interrupted_handler=None):

        self._client_timeout_handler = client_timeout_handler
        self._client_disconnect_handler = client_disconnect_handler
        self._client_interrupted_handler = client_interrupted_handler

        self._server_socket = None
        self._client_socket = None
        self._running = True

    def initialize(self):

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

    def run(self):

        while self._running:

            # wait for client connection if client not connected
            if self._client_is_disconnected():
                self._wait_for_client_connection()

            # attempt to read client message
            try:
                client_message = self._client_socket.recv(PingPongServer.SERVER_RECEIVE_BUFFER_SIZE)
            except socket.timeout:
                if self._client_timeout_handler:
                    self._client_timeout_handler()
                break

            if client_message == '':
                if self._client_disconnect_handler:
                    self._client_disconnect_handler()
                self._clear_client_socket()
                break

            if client_message == 'ping':
                # attempt to send pong
                message = 'pong ({})'.format(time.time())

                try:
                    self._client_socket.send(message)
                except IOError:
                    if self._client_interrupted_handler:
                        self._client_interrupted_handler()
                    self._clear_client_socket()

    def _client_is_disconnected(self):
        return self._client_socket is None

    def _wait_for_client_connection(self):
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

