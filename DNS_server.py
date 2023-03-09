import socket
import pickle
import threading

DNS_PORT = 5555
SERVER_PORT = 30015
SERVER_IP = socket.gethostbyname(socket.gethostname())

DNS_IP = socket.gethostbyname(socket.gethostname())  # getting the ip of the computer
ADDR = (DNS_IP, DNS_PORT)
FORMAT = 'utf-8'  # the format that the messages decode/encode
CHUNK = 32
LEN_HEADER_SIZE = 8
DISCONNECT_MESSAGE_DNS = "EXIT"

server_addr = pickle.dumps((SERVER_IP, SERVER_PORT))
mapper = {"SERVER": server_addr}

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

                if full_msg == DISCONNECT_MESSAGE_DNS:
                    print("disconnecting from", addr)
                    break

                # answer
                answer = pickle.dumps("I am sorry, I couldn't find the destination address")
                if full_msg in mapper:
                    answer = mapper[full_msg]
                answer = bytes(f'{len(answer) :< {LEN_HEADER_SIZE}}', FORMAT) + answer
                print("sending response", end="\n\n")
                conn.send(answer)

                # preparing for the next message
                get_size = LEN_HEADER_SIZE
                full_msg = b''
                new_msg = True
    conn.close()


def start():
    print("DNS server is starting...")
    server.listen(5)
    print(f"Server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()  # while accepting new client - receiving socket,address

        # creating thread for each client so multiple clients will be able to connect simultaneously
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


start()
