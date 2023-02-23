# [name,age,Team, position, goals, assissts]
import socket
import threading
import pickle
from PL_player import PL_player
import query_object

# todo synchronized data/ or maybe not ?
data = [PL_player("Erling Haaland", 22, "MCFC", "CF", 26, 4),
        PL_player("Harry Kane", 29, "Spurs", "CF", 17, 2),
        PL_player("Ivan Toney", 26, "Brentford", "CF", 14, 3),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        PL_player("Bukayo Saka", 21, "Arsenal", "RF", 9, 8),
        ]

HEADERSIZE = 16
PORT = 5056
SERVER = socket.gethostbyname(socket.gethostname())  # getting the ip of the computer
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'  # the format that the messages decode/encode


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP socket
server.bind(ADDR)  # binding the address


def handle_client(conn, addr):
    print(f"new connection with {addr} ")
    full_msg = b''
    connected = True
    new_msg = True
    msg_len = 0
    while connected:
        msg = conn.recv(16)
        if msg:
            if new_msg:
                msg_len = int(msg[:HEADERSIZE])  # converting the length to int
                print("the massage length:", msg_len)  # printing the length

                new_msg = False
            else:
                full_msg += msg

            if len(full_msg) == msg_len:
                print("full message received!")

                full_msg = pickle.loads(full_msg)
                if full_msg[0].is_exit():
                    print("disconnecting from", addr)
                    break
                answer = filter_by_queries(full_msg)
                answer = pickle.dumps(answer)
                answer = bytes(f'{len(answer) :< {HEADERSIZE}}', FORMAT) + answer
                conn.send(answer)

                full_msg = b''
                new_msg = True
    conn.close()


def start():
    print("server is starting...")
    server.listen(5)
    print(f"Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()  # while accepting new client - receiving socket,address

        # creating thread for each client so multiple clients will be able to connect simultaneously
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


def filter_by_queries(queries: list[query_object.query_obj]) -> list[PL_player]:
    filtered_data = data
    for q in queries:
        filtered_data = q.do_query(filtered_data)
    return filtered_data


start()
