import errno
import logging
import socket
import time


# logging
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger('pingpongserver')
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(CONSOLE_HANDLER)

# server variables
SERVER_SOCKET_BACKLOG = 5
SERVER_PORT = 9999
SERVER_RUNNING = True
SERVER_RECEIVE_BUFFER_SIZE = 1024
CLIENT_SOCKET_TIMEOUT_SECONDS = 5


def wait_for_client_connection(server_socket):
    """
    Wait for a client connection on the given server socket
    """

    LOGGER.info('Waiting for connection')

    (client_socket, client_address) = server_socket.accept()
    LOGGER.info('Received connection from %s', client_address[0])

    client_socket.settimeout(CLIENT_SOCKET_TIMEOUT_SECONDS)
    return client_socket


def read_client_message(client_socket):
    """
    Read a message from the given socket
    """

    LOGGER.info('Waiting for client message')

    try:
        client_message = client_socket.recv(SERVER_RECEIVE_BUFFER_SIZE)
    except socket.timeout:
        LOGGER.info('Timed out waiting for message')
        return None

    if client_message == '':
        LOGGER.info('Detected disconnect while waiting for message')
        return None
    else:
        LOGGER.info('Received client message: "%s"', client_message)
        return client_message


def main():
    """
    MAIN
    """

    # stateful variables
    client_connection = None

    # create the server socket
    LOGGER.info('Creating server socket')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind to the host:port
    host = socket.gethostname()
    port = SERVER_PORT
    LOGGER.info('Binding to %s:%d', host, port)
    server_socket.bind((host, port))

    # listen for connections
    server_socket.listen(SERVER_SOCKET_BACKLOG)

    # main
    while SERVER_RUNNING:

        # wait for client connection if client not connected
        if client_connection is None:
            client_connection = wait_for_client_connection(server_socket)

        # attempt to read client message
        client_message = read_client_message(client_connection)

        if client_message is not None:

            # client sent ping message
            if client_message == 'ping':

                # attempt to send pong
                message = 'pong ({})'.format(time.time())

                try:
                    LOGGER.info('Sending "%s"', message)
                    client_connection.send(message)
                except IOError, error:
                    if error.errno == errno.EPIPE:
                        LOGGER.info('Detected disconnect')
                        client_connection = None

            # client sent unknown message
            else:
                LOGGER.info('Received unknown message: "%s"', client_message)

        # client disconnected
        else:
            client_connection = None


if __name__ == '__main__':
    main()
