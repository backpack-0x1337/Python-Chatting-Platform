import threading
import time
from config import *

# SERVER = "1.132.104.202"

SERVER = HOST
print(SERVER)
# print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def isPasswordValid(to_check_password):
    if to_check_password:
        return int(to_check_password) == PASSWORD
    return False


def send_to_clients(msg):
    msg_size = len(msg)
    for client_connection in client_list:
        send_to_client(client_connection, msg)


def send_to_client(client_connection, msg):
    # first send header which is the length of message
    message = msg.encode(FORMAT)
    send_length = len(message)
    header_message = str(send_length).encode(FORMAT)
    header_message += b' ' * (HEADER - len(header_message))
    client_connection.send(header_message)
    client_connection.send(message)

def receive_from_client(conn):
    msg = ''
    try:
        # connected = True
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length and msg_length != 0:
            msg = conn.recv(int(msg_length)).decode(FORMAT)
            # if msg == DISCONNECT_MESSAGE:
            #     connected = False
            return msg
        return None
    except Exception:
        return msg
    # receive_from_client(conn)

        # print(f"[{addr}]{msg}")

def handle_client(conn, addr):

    print(f"[NEW CONNECTION]{addr} connected.")
    # ask client name
    # check whether password is valid! (in utf-8 format)
    # receive_from_client(conn)
    # time.sleep(1)
    send_to_client(conn, "Hey you Welcome! Enter the password to continue!")
    password = receive_from_client(conn)
    while not password:
        password = receive_from_client(conn)
    if isPasswordValid(password):
        print(f"{addr} given right password!")
        send_to_client(conn, ERROR_OK)
    else:
        print(f"{addr} given wrong password disconnecting!")
        send_to_client(conn, DISCONNECT_MESSAGE)
        # send_to_client(conn, "You password is incorrect! SEE YA")
        time.sleep(1)
        conn.close()
        exit()

    send_to_client(conn, "What is you name? : ")
    client_name = receive_from_client(conn)
    while not client_name:
        client_name = receive_from_client(conn)
    send_to_client(conn, ERROR_OK)
    print(f"{client_name} has joined")
    send_to_clients(f"{client_name} has joined")

    connected = True
    while connected:
        msg = receive_from_client(conn)
        if msg == DISCONNECT_MESSAGE:
            print(f"{client_name}: {msg}")
            break
        send_to_clients(f"{client_name}: {msg}")
        print(f"{client_name}: {msg}")
    send_to_clients(f"{client_name} left the chat.")
    client_list.remove(conn)
    send_to_client(conn, DISCONNECT_MESSAGE)
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Chatting server is starting")

    try:
        while True:
            conn, addr = server.accept()
            client_list.append(conn)
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTION]{threading.active_count() - 1}")
    except Exception:
        server.close()
        print(f"[CLOSING] Chatting server is CLOSING")




client_list = []
PASSWORD = int(input("What would you like your password as? (int): "))
start()
