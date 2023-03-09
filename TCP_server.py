# [name,rating,Team, position, goals, assissts]
import socket
import threading
import pickle
from PL_player import PL_player
import query_object
import DATA

LEN_HEADER_SIZE = 8
PORT = 30015
SERVER = socket.gethostbyname(socket.gethostname())  # getting the ip of the computer
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'  # the format that the messages decode/encode
CHUNK = 32

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
                if full_msg != [] and full_msg[0].is_exit():
                    print("disconnecting from", addr)
                    break
                answer = filter_by_queries(full_msg)
                answer = pickle.dumps(answer)
                # :< fill (pad) all the header
                # (because can be case that the header is 8  and the len pf answer is 1000 so 4 characters missed)
                answer = bytes(f'{len(answer) :< {LEN_HEADER_SIZE}}', FORMAT) + answer
                print("sending response", end="\n\n")
                conn.send(answer)
                get_size = LEN_HEADER_SIZE
                full_msg = b''
                new_msg = True
    conn.close()


def start():
    print("server is starting...")
    server.listen(5)
    print(f"Server is listening on {ADDR}")
    while True:
        conn, addr = server.accept()  # while accepting new client - receiving socket,address

        # creating thread for each client so multiple clients will be able to connect simultaneously
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


def filter_by_queries(queries: list[query_object.query_obj]) -> list[PL_player]:
    filtered_data = DATA.data
    for q in queries:
        filtered_data = q.do_query(filtered_data)
    return filtered_data


start()
