import socket

HEADER = 64
PORT = 5500
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = '192.168.101.130'
# SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    header_message = str(msg_length).encode(FORMAT)
    header_message += b' ' * (HEADER - len(header_message))
    client.send(header_message)
    client.send(message)


send("Hello Bro")
send(DISCONNECT_MESSAGE)
