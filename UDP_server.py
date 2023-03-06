import socket
import threading
from PL_player import PL_player
import query_object
import functions
import DATA

LEN_SIZE_HEADER = 8
LEN_INDEX_HEADER = 8
PORT = 6060
SERVER_IP = socket.gethostbyname(socket.gethostname())  # getting the ip of the computer
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'  # the format that the messages decode/encode
CHUNK = 128

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
server.bind(ADDR)  # binding the address
clients = []  # todo: synchronized
PORT_CHANGE = 1  # todo: synchronized


def handle_client(ip, port):
    addr = (ip, port)
    print(f"new connection with {addr} ")
    full_msg = b''


    # creating new socket for this client
    current_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    current_port = PORT + PORT_CHANGE
    # todo: port_change++ synchronized
    current_addr = (SERVER_IP, current_port)

    # free the port right after disconnecting
    current_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    current_sock.bind(current_addr)

    # sending the message for the client to know the new port
    start_msg = bytes(' ', FORMAT)
    current_sock.sendto(start_msg, addr)

    while True:
        full_msg = functions.receive(current_sock, addr)

        # EXIT message
        if full_msg != [] and full_msg[0].is_exit():
            print("disconnecting from", addr)
            clients.remove(addr)  # todo: synchronized
            break

        answer = filter_by_queries(full_msg)

        print("sending response", end="\n\n")
        # sending answer
        functions.send_with_cc(current_sock, addr, answer)
        full_msg = b''


# def send_with_cc(cur_sock, addr, msg):
#     window_size = 1
#     window_index = 0
#     time_limit = 5
#     # turning the socket to non-blocking
#     cur_sock.setblocking(0)
#
#     bytes_rec = 0
#     index = 0
#     chunks = []
#     while bytes_rec <= len(msg):
#         chunks.insert(0, bytes(f'{len(msg) :< {LEN_SIZE_HEADER}}', FORMAT) +
#                       bytes(f'{index :< {LEN_INDEX_HEADER}}', FORMAT) + msg[bytes_rec:bytes_rec + CHUNK])
#         index += 1
#         bytes_rec += CHUNK
#     chunks.reverse()
#
#     state = [0 for _ in chunks]
#     timestemps = [0.0 for _ in chunks]
#     dup_ack = [-1, 0]  # [ack index , ack counter]
#     while True:
#         # send window and update timestemp
#         for i in range(window_index, window_index + window_size):
#             if state[i] == 0:
#                 cur_sock.sendto(chunks[i], addr)
#                 timestemps[i] = time.time()
#         # recv acks -for every ack (1) increase window (2)move window (3) mark as true
#         for _ in range(window_size):
#             try:
#                 ack = cur_sock.recvfrom(4)[0]
#                 ack = int(ack)
#                 if ack == dup_ack[0]:
#                     dup_ack[1] += 1
#                 else:
#                     dup_ack[0] = ack
#                     dup_ack[1] = 0
#                 if dup_ack[1] >= 3:  # LATENCY!
#                     window_size /= 2
#                     cur_sock.sendto(chunks[ack], addr)
#                 else:
#                     for i in range(window_index, ack + 1):
#                         if state[i] != 2:
#                             state[i] = 2
#                             window_size = increase_window(window_size)
#
#                     while state[window_index] == 2:
#                         window_index += 1
#
#             except socket.error as e:
#                 continue
#
#         # check timers
#         for i in range(window_index, window_index + window_size):
#             if state[i] == 1:
#                 if time.time() - timestemps[i] >= time_limit:  # TIMEOUT!
#                     window_size = 1
#
#         if state[-1] == 2:
#             cur_sock.setblocking(1)
#             break
#
#
# def increase_window(window_size):
#     if window_size < 16:
#         return window_size * 2
#     else:
#         window_size += 1
#
#
# def receive(cur_sock, addr):
#     new_msg = True
#     get_size = CHUNK
#     max_seq_index = 0
#     chunks = []
#     indexes = []
#     msg_len = 0
#     bytes_received = 0
#
#     while True:
#         msg = cur_sock.recvfrom(get_size)[0]
#         if msg:
#             msg_len = int(msg[:LEN_SIZE_HEADER])
#             index = int(msg[LEN_SIZE_HEADER:LEN_INDEX_HEADER])
#
#             if max_seq_index == index:
#                 max_seq_index += 1
#             indexes.insert(0, index)
#             while max_seq_index in indexes:
#                 max_seq_index += 1
#             chunks.insert(0, msg)
#             bytes_received += len(msg[LEN_SIZE_HEADER + LEN_INDEX_HEADER:])
#
#             # sending ACK
#             cur_sock.sendto(bytes(max_seq_index), addr)  # todo: padding needed?
#
#         if bytes_received == msg_len:
#             # sort chunks by index
#             chunks = sorted(chunks, key=lambda chunk_: chunk_[LEN_SIZE_HEADER:LEN_INDEX_HEADER], reverse=False)
#             # combine chunks
#             full_msg = b''
#             for chunk in chunks:
#                 full_msg += chunk[LEN_SIZE_HEADER + LEN_INDEX_HEADER:]
#             return full_msg


def start():
    print(f"UDP server is listening on {SERVER_IP}")
    print("One should send start message before sending data!")
    while True:
        bytes_Address_Pair = server.recvfrom(1)
        addr = bytes_Address_Pair[1]

        # creating thread for each client so multiple clients will be able to connect simultaneously
        if addr not in clients:
            clients.insert(0, addr)
            thread = threading.Thread(target=handle_client, args=(addr))
            print("My clients right now:", end="[ ")
            for x in clients:
                print(x, end=", ")
            print("]")
            thread.start()


def filter_by_queries(queries: list[query_object.query_obj]) -> list[PL_player]:
    filtered_data = DATA.data
    for q in queries:
        filtered_data = q.do_query(filtered_data)
    return filtered_data


start()
