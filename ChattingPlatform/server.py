import socket
import threading
import time

HEADER = 64
PORT = 55001
INFO_SIZE = 1024
# SERVER = "1.132.104.202"

SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
# todo get ipaddress
# print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECTED'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def isPasswordValid(to_check_password):
    return to_check_password == PASSWORD


def send_to_clients(msg):
    msg_size = len(msg)
    for client_connection in client_list:
        client_connection.send(msg_size).encode(FORMAT)
        client_connection.send(msg).encode(FORMAT)


def send_to_client(client_connection, msg):
    # first send header which is the length of message
    client_connection.send(str(len(msg))).encode(FORMAT)
    client_connection.send(msg).encode(FORMAT)


def receive_from_client(conn):
    connected = True
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg = conn.recv(int(msg_length)).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
        return connected, msg
        # print(f"[{addr}]{msg}")

def handle_client(conn, addr):
    print(f"[NEW CONNECTION]{addr} connected.")
    # ask client name
    # check whether password is valid! (in utf-8 format)
    send_to_client(conn, "Hey you Welcome! Enter the password to continue!")
    password = int(conn.recv(INFO_SIZE).decode(FORMAT))
    if not isPasswordValid(password):
        conn.send("You password is incorrect! SEE YA")

    send_to_client(conn, "What is you name? : ")
    client_name = conn.recv(INFO_SIZE).decode(FORMAT)
    send_to_clients(f"{client_name} has joined")

    connected = True
    while connected:
        connected, msg = receive_from_client(conn)
        send_to_clients(f"{client_name}: {msg}")
    send_to_clients(f"{client_name} left the chat.")
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Chatting server is starting")
    while True:
        conn, addr = server.accept()
        client_list.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTION]{threading.active_count() - 1}")


client_list = []
PASSWORD = int(input("What would you like your password as? (int): "))
start()
