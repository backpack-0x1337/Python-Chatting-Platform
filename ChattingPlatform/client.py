import threading
from time import sleep

from config import *
from os import wait

SERVER = socket.gethostbyname(HOST_NAME)
ADDR = (SERVER, PORT)

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECTED'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
kill = False


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    wait()
    # print(client.recv(2048).decode(FORMAT))


def send_message(conn, msg):
    msg_length = str(len(msg))
    conn.send(msg_length.encode(FORMAT))
    sleep(0.1)
    conn.send(msg.encode(FORMAT))


def handle_sending(conn):
    try:
        while True:
            message = input("")
            send_message(conn, message)
            # print("message sent")
            if kill is True:
                exit()
    except Exception:
        print(Exception)
        exit()

def handle_receiving(conn):
    try:
        while True:
            msg = receive_from_server(conn)
            if msg == DISCONNECT_MESSAGE:
                print("Disconnect by host")
                break
            else:
                print(msg)
    except Exception:
        print(Exception)
        exit()

def receive_from_server(server):
    msg_length = server.recv(HEADER).decode(FORMAT)
    if msg_length and msg_length != 0:
        msg = server.recv(int(msg_length)).decode(FORMAT)
    # print(msg)
        return msg
    return None


def verify_password():
    msg = receive_from_server(client)
    print(msg)
    send_message(client, input())
    msg = receive_from_server(client)
    print(msg)
    if msg == DISCONNECT_MESSAGE:
        print("You password is incorrect! SEE YA")
        return False
    if msg == ERROR_OK:
        print("You password is correct!")
        return True
    verify_password()
def set_name():
    msg = receive_from_server(client)
    print(msg)
    send_message(client, input())
    msg = receive_from_server(client)
    print(msg)
    if msg == DISCONNECT_MESSAGE:
        print("You name is not ok!")
        return False
    if msg == ERROR_OK:
        print("You name is ok!")
        return True
def main():
    # thr
    # client.listen()
    try:
        print(f"[LISTENING] client is starting")
        # conn = client
        sleep(1)
        if verify_password() and set_name():
            # make one thread for receiving message and one for sending message
            receive_thread = threading.Thread(target=handle_receiving, args=(client,))
            receive_thread.start()

            sending_thread = threading.Thread(target=handle_sending, args=(client,))
            sending_thread.start()

            receive_thread.join()
        client.close()

    except Exception:
        client.close()
main()
print(f"[CLOSING] Client is CLOSING")
