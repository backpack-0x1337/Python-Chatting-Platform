import socket

HEADER = 258
# PORT = "PORT U WISH TO USE 5000-10000"
PORT = 33322
# HOST = "YOUR PUBLIC IP"
HOST = socket.gethostbyname(socket.gethostname())
DISCONNECT_MESSAGE = '!DISCONNECTED'
ERROR_OK = 'ERROR_OK'
