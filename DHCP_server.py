import socket
import pickle
import threading

DHCP_PORT = 4836
DNS_PORT = 5555
CLIENT_PORT = 20351  # (for UDP)
data_for_client = [(socket.gethostbyname(socket.gethostname()), CLIENT_PORT),
                   (socket.gethostbyname(socket.gethostname()), DNS_PORT)]

data_for_client = pickle.dumps(data_for_client)

DHCP_IP = socket.gethostbyname(socket.gethostname())  # getting the ip of the computer
ADDR = (DHCP_IP, DHCP_PORT)
FORMAT = 'utf-8'  # the format that the messages decode/encode
CHUNK = 32
LEN_HEADER_SIZE = 8
DISCONNECT_MESSAGE_DHCP = "EXIT"
CONNECTION_MESSAGE = "PLEASE CONNECT ME"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
server.bind(ADDR)  # binding the address


def handle_client(conn, addr):
    print(f"new connection with {addr} ")
    full_msg = b''
    connected = True
    new_msg = True
    msg_len = 0
    get_size = LEN_HEADER_SIZE
    while connected:
        msg = conn.recv(get_size)
        if msg:
            if new_msg:
                msg_len = int(msg[:LEN_HEADER_SIZE])  # converting the length to int
                print("the massage length:", msg_len)  # printing the length
                get_size = CHUNK
                new_msg = False
            else:
                full_msg += msg

            if len(full_msg) == msg_len:
                print("full message received!")
                print("processing request...")
                full_msg = pickle.loads(full_msg)

                if full_msg == DISCONNECT_MESSAGE_DHCP:
                    print("disconnecting from", addr)
                    break

                if full_msg == CONNECTION_MESSAGE:
                    answer = bytes(f'{len(data_for_client) :< {LEN_HEADER_SIZE}}', FORMAT) + data_for_client
                    print("sending response", end="\n\n")
                    conn.send(answer)

                get_size = LEN_HEADER_SIZE
                full_msg = b''
                new_msg = True
    conn.close()


def start():
    print("DHCP server is starting...")
    server.listen(5)
    print(f"Server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()  # while accepting new client - receiving socket,address

        # creating thread for each client so multiple clients will be able to connect simultaneously
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start()
