import errno
import logging
import socket
import time


# logging
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setLevel(logging.DEBUG)
CONSOLE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger('ping-pong-server')
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(CONSOLE_HANDLER)

# server variables
SERVER_SOCKET_BACKLOG = 5
SERVER_PORT = 9999
SERVER_RUNNING = True
SERVER_INTERVAL_SECONDS = 1


#-------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------
def main():

    global LOGGER
    global SERVER_SOCKET_BACKLOG
    global SERVER_PORT
    global SERVER_RUNNING

    # stateful variables
    client_connection = None

    # create the server socket
    LOGGER.info('Creating server socket')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind to the host:port
    host = socket.gethostname()
    port = SERVER_PORT
    LOGGER.info('Binding to {}:{}'.format(host, port))
    server_socket.bind((host, port))

    # listen for connections
    server_socket.listen(SERVER_SOCKET_BACKLOG)

    # main
    while SERVER_RUNNING:

        # wait for a client connection if not connected
        if client_connection is None:
            LOGGER.info('Waiting for connection')

            # establish connection with client
            (new_client_connection, client_address) = server_socket.accept()
            LOGGER.info('Received connection from {}'.format(client_address[0]))
            client_connection = new_client_connection

        # attempt to send message
        message = '{}: Hi'.format(time.time())

        try:
            # TODO: check bytes sent (return value from send)
            LOGGER.info('Sending message "{}"'.format(message))
            client_connection.send(message)
        except IOError, e:
            # TODO: handle other IOErrors
            if e.errno == errno.EPIPE:
                LOGGER.info('Detected disconnect')
                client_connection = None

        # rest
        time.sleep(SERVER_INTERVAL_SECONDS)


if __name__ == '__main__':
    main()
