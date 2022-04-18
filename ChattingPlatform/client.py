import socket

HEADER = 64
PORT = 55001
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECTED'


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    # print(client.recv(2048).decode(FORMAT))


def send_message(conn, msg):
    msg_length = str(len(msg))
    conn.send(msg_length.encode(FORMAT))
    conn.send(msg.encode(FORMAT))


def handle_sending(conn, addr):
    password = input("What is the password? ")
    send_message(conn, password)


def handle_receiving(conn, addr):
    connect = True
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg = conn.recv(int(msg_length)).decode(FORMAT)


def main():
    # thr
    client.listen()
    print(f"[LISTENING] client is starting")
    while True:
        conn, addr = client.accept()
        # make one thread for receiving message and one for sending message
        sending_thread = threading.Thread(target=handle_sending, args=(conn, addr))
        sending_thread.start()
        # receive_thread = threading.Thread(target=handle_receiving, args=(conn, addr))
        # receive_thread.start()


main()
