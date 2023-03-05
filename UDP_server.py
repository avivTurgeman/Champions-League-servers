import socket
import threading
import pickle
from PL_player import PL_player
import query_object
import functions

# [name,rating,Team, position, goals, assists]
data = [
    # Manchester City F.C.
    PL_player("Erling Haaland", 7.8, "MCFC", "CF", 5, 0),
    PL_player("Julián Álvarez", 7.2, "MCFC", "CF", 2, 2),
    PL_player("Jack Grealish", 7.3, "MCFC", "LF", 0, 0),
    PL_player("Ilkay Gündoğan", 7.2, "MCFC", "CM", 0, 1),
    PL_player("Rodri Hernández", 6.8, "MCFC", "CM", 0, 0),
    PL_player("Phil Foden", 7.4, "MCFC", "AM", 1, 0),
    PL_player("Rico Lewis", 7.2, "MCFC", "RB", 1, 0),
    PL_player("Nathan Aké", 7.0, "MCFC", "CB", 0, 0),
    PL_player("Ruben Dias", 7.2, "MCFC", "CB", 1, 0),
    PL_player("Manuel Akanji", 7.0, "MCFC", "CB", 0, 0),
    PL_player("Ederson Moraes", 7.0, "MCFC", "GK", 0, 0),

    # Liverpool F.C.
    PL_player("Mohamed Salah", 8.0, "Liverpool", "RF", 8, 2),
    PL_player("Roberto Firmino", 7.1, "Liverpool", "CF", 2, 1),
    PL_player("Cody Gakpo", 7.1, "Liverpool", "LF", 0, 1),
    PL_player("James Milner", 6.1, "Liverpool", "CM", 0, 0),
    PL_player("Jordan Henderson", 6.9, "Liverpool", "CM", 0, 1),
    PL_player("Fabinho", 6.5, "Liverpool", "CM", 0, 0),
    PL_player("Alexander Arnold", 7.2, "Liverpool", "RB", 1, 0),
    PL_player("Virgil van Dijk", 6.8, "Liverpool", "CB", 0, 0),
    PL_player("Joel Matip", 7.2, "Liverpool", "CB", 1, 0),
    PL_player("Andrew Robertson", 7.0, "Liverpool", "LB", 0, 2),
    PL_player("Alisson Becker", 6.5, "Liverpool", "GK", 0, 0),

    # Real Madrid F.C.
    PL_player("Vinicius Júnior", 7.7, "RMFC", "LF", 6, 2),
    PL_player("Karim Benzema", 7.6, "RMFC", "CF", 2, 1),
    PL_player("Rodrygo", 7.8, "RMFC", "RF", 3, 2),
    PL_player("Luka Modric", 7.4, "RMFC", "CM", 2, 1),
    PL_player("Camavinga", 6.5, "RMFC", "CM", 0, 0),
    PL_player("Valverde", 7.9, "RMFC", "CM", 2, 2),
    PL_player("David Alaba", 6.9, "RMFC", "CB", 0, 0),
    PL_player("Antonio Rüdiger", 7.0, "RMFC", "CB", 1, 0),
    PL_player("Éder Militão", 7.1, "RMFC", "CB", 1, 0),
    PL_player("Daniel Carvajal", 6.9, "RMFC", "RB", 0, 2),
    PL_player("Thibaut Courtois", 7.2, "RMFC", "GK", 0, 0),

    # Paris Saint-Germain F.C.
    PL_player("Kylian Mbappe", 7.8, "PSG", "CF", 7, 3),
    PL_player("Lionel Messi", 8.4, "PSG", "RF", 4, 4),
    PL_player("Neymar", 7.6, "PSG", "LF", 2, 2),
    PL_player("Carlos Soler", 7.1, "PSG", "CM", 1, 0),
    PL_player("Marco Verratti", 6.5, "PSG", "CM", 0, 1),
    PL_player("Fabián Ruiz", 6.6, "PSG", "CM", 0, 0),
    PL_player("Nuno Mendes", 6.8, "PSG", "LB", 1, 0),
    PL_player("Sergio Ramos", 6.9, "PSG", "CB", 0, 0),
    PL_player("Marquinhos", 6.8, "PSG", "CB", 0, 0),
    PL_player("Achraf Hakimi", 6.7, "PSG", "RB", 0, 2),
    PL_player("Donnarumma", 6.7, "PSG", "GK", 0, 0),

    # FC Bayren Munich
    PL_player("Choupo-Moting", 7.3, "FCBM", "CF", 3, 0),
    PL_player("Sadio Mané", 7.5, "FCBM", "LF", 3, 1),
    PL_player("Kingsley Coman", 7.7, "FCBM", "LF", 1, 1),
    PL_player("Leroy Sané", 7.9, "FCBM", "RF", 4, 1),
    PL_player("Leon Goretzka", 7.3, "FCBM", "CM", 2, 3),
    PL_player("Joshua Kimmich", 7.9, "FCBM", "CM", 0, 3),
    PL_player("João Cancelo", 7.3, "FCBM", "RB", 0, 3),
    PL_player("João Cancelo", 7.1, "FCBM", "CB", 0, 0),
    PL_player("Dayot Upamecano", 7.1, "FCBM", "CB", 0, 0),
    PL_player("Benjamin Pavard", 7.3, "FCBM", "RB", 2, 0),
    PL_player("Yann Sommer", 7.9, "FCBM", "GK", 0, 0),

    # FC Porto
    PL_player("Mehdi Taremi", 8.0, "Porto", "CF", 5, 2),
    PL_player("Wenderson Galeno", 7.3, "Porto", "LF", 2, 1),
    PL_player("Pepê", 6.7, "Porto", "LF", 0, 0),
    PL_player("Otavio", 6.3, "Porto", "CM", 0, 2),
    PL_player("Mateus Uribe", 6.7, "Porto", "CM", 1, 0),
    PL_player("Marko Grujić", 6.9, "Porto", "CM", 0, 0),
    PL_player("Iván Marcano", 6.3, "Porto", "CB", 0, 0),
    PL_player("Pepe", 6.9, "Porto", "CB", 0, 0),
    PL_player("Joao Mario", 6.3, "Porto", "LB", 0, 0),
    PL_player("Zaidu Sanusi", 6.9, "Porto", "LB", 1, 0),
    PL_player("Diogo Costa", 7.7, "Porto", "GK", 0, 0)
]

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
        answer = pickle.dumps(answer)
        # :< fill (pad) all the header
        # (because can be case that the header is 8  and the len pf answer is 1000 so 4 characters missed)

        # current_sock.sendto(bytes(f'{len(answer) :< {LEN_SIZE_HEADER}}', FORMAT), addr)
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
    filtered_data = data
    for q in queries:
        filtered_data = q.do_query(filtered_data)
    return filtered_data


start()
