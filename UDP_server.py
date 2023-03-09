import pickle
import socket
import threading
import time
from PL_player import PL_player
import query_object
import functions
import DATA

PORT = 30015
SERVER_IP = socket.gethostbyname(socket.gethostname())  # getting the ip of the computer
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'  # the format that the messages decode/encode
CHUNK = 32

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP socket
server.bind(ADDR)  # binding the address
clients = []
PORT_CHANGE = 1
change_port_lock = threading.Lock()
clients_lock = threading.Lock()


def handle_client(ip, port):
    addr = (ip, port)
    print(f"\nnew connection with {addr} ", end="\n\n")
    full_msg = b''

    # creating new socket for this client
    current_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    current_port = get_change_port() + PORT
    current_addr = (SERVER_IP, current_port)

    # free the port right after disconnecting
    current_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    current_sock.bind(current_addr)

    # sending the message for the client to know the new port
    flag = 1
    current_sock.setblocking(False)
    while flag:
        if flag == 1:
            current_sock.settimeout(0.3)
            # syn ack
            print("sending SYN-ACK")
            start_msg = pickle.dumps("ack")
            current_sock.sendto(start_msg, addr)
            flag = 2

        if flag == 2:
            msg = 0
            try:
                current_sock.settimeout(0.6)
                if msg == 0:
                    msg = current_sock.recvfrom(100)
            except socket.error as e:
                print(e)

            if msg != 0:
                msg = pickle.loads(msg[0])
                print("msg:" ,msg,"len",len(msg) )
                if msg == "ack":
                    print(f'connection with {addr} established')
                    flag = 0
                    break
                else:
                    flag = 1
            else:
                flag = 1
    current_sock.setblocking(True)
    current_sock.settimeout(30.0)

    while True:
        full_msg = functions.receive(current_sock, addr)

        # EXIT message
        if full_msg != [] and full_msg[0].is_exit():
            print("disconnecting from", addr)
            remove_client(addr)
            print("My clients right now:", end="[ ")
            for x in clients:
                print(x, end=", ")
            print("]")
            break

        answer = filter_by_queries(full_msg)

        print("sending response", end="\n\n")
        # sending answer
        functions.send_with_cc(current_sock, addr, answer)
        full_msg = b''


def start():
    print(f"UDP server is listening on {SERVER_IP}")
    print("One should send start message before sending data!")
    while True:
        # syn
        bytes_Address_Pair = server.recvfrom(100)
        addr = bytes_Address_Pair[1]

        # creating thread for each client so multiple clients will be able to connect simultaneously
        if addr not in clients:
            add_client(addr)
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


def get_change_port() -> int:
    global PORT_CHANGE
    change_port_lock.acquire()
    ans = PORT_CHANGE
    PORT_CHANGE += 1
    change_port_lock.release()
    return ans


def add_client(client):
    clients_lock.acquire()
    clients.insert(0, client)
    clients_lock.release()


def remove_client(client):
    clients_lock.acquire()
    clients.remove(client)
    clients_lock.release()


start()
