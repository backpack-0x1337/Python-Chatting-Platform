import socket
import threading
import time

HEADER = 64

# save bet is to run a port above 4000 because they are unactive
PORT = 5050

# local ipv4
# SERVER = "10.89.125.66"
SERVER = socket.gethostbyname(socket.gethostname())

# Bind them in a tuple
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# Pick the port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # blocking line of code
        # will not process unless receive content
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg = conn.recv(int(msg_length)).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                # conn.send("BYE").encode(FORMAT)
                connected = False
            print(f"[{addr}]{msg}")
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING Server is listining {ADDR}" )
    while True:
        # this line will block
        # store where it come from and what port
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")



print("[STARTING] server starting")
start()
