import pickle
import socket
import time


LEN_SIZE_HEADER = 8
LEN_INDEX_HEADER = 8
ACK_SIZE = 8
FORMAT = 'utf-8'  # the format that the messages decode/encode
CHUNK = 128


def send_with_cc(cur_sock, addr, msg):
    # msg = pickle.dumps(msg)
    window_size = 1
    window_index = 0
    time_limit = 5
    dup_limit = 250
    # turning the socket to non-blocking
    cur_sock.setblocking(0)

    bytes_rec = 0
    index = 0
    chunks = []
    while bytes_rec <= len(msg):
        chunks.insert(0, bytes(f'{len(msg) :< {LEN_SIZE_HEADER}}', FORMAT) +
                      bytes(f'{index :< {LEN_INDEX_HEADER}}', FORMAT) + msg[bytes_rec:bytes_rec + CHUNK])
        index += 1
        bytes_rec += CHUNK
    chunks.reverse()
    print("chunks", chunks)

    state = [0 for _ in chunks]
    timestemps = [0.0 for _ in chunks]
    dup_ack = [-1, 0]  # [ack index , ack counter]
    while True:
        # send window and update timestemp
        for k in range(window_index, window_index + window_size):
            if k < len(state):
                if state[k] == 0:
                    cur_sock.sendto(chunks[k], addr)
                    timestemps[k] = time.time()
        # recv acks -for every ack (1) increase window (2)move window (3) mark as true
        for _ in range(window_size):
            try:
                ack = cur_sock.recvfrom(ACK_SIZE)[0]
                ack = int(ack)
                if ack == dup_ack[0]:
                    dup_ack[1] += 1
                else:
                    dup_ack[0] = ack
                    dup_ack[1] = 0
                if dup_ack[1] >= dup_limit:  # LATENCY!
                    print("dup_ack [", dup_ack[0], dup_ack[1], "]")
                    window_size = max(int(window_size / 2), 1)
                    cur_sock.sendto(chunks[ack], addr)
                else:
                    for k in range(window_index, ack):
                        if state[k] != 2:
                            state[k] = 2
                            window_size = increase_window(window_size)

                    if state[-1] == 2:
                        cur_sock.setblocking(1)
                        break

                    while state[window_index] == 2:
                        window_index += 1

            except socket.error as e:
                continue

        # check timers
        for k in range(window_index, window_index + window_size):
            if k < len(state):
                if state[k] == 1:
                    if time.time() - timestemps[k] >= time_limit:  # TIMEOUT!
                        window_size = 1

        if state[-1] == 2:
            cur_sock.setblocking(1)
            break


def increase_window(window_size):
    if window_size < 16:
        return window_size * 2
    else:
        return window_size + 1


def receive(cur_sock, addr) -> list:
    get_size = CHUNK + LEN_SIZE_HEADER + LEN_INDEX_HEADER
    max_seq_index = 0
    chunks = []
    indexes = []
    msg_len = 0
    bytes_received = 0
    cur_sock.setblocking(1)
    while True:
        msg = 0
        msg = cur_sock.recvfrom(get_size)[0]
        print("msg:", msg)
        if msg:
            msg_len = int(msg[:LEN_SIZE_HEADER])
            index = int(msg[LEN_SIZE_HEADER:LEN_INDEX_HEADER + LEN_SIZE_HEADER])

            if index not in indexes:
                bytes_received += len(msg[LEN_SIZE_HEADER + LEN_INDEX_HEADER:])
                chunks.insert(0, msg)

            if max_seq_index == index:
                max_seq_index += 1
            indexes.insert(0, index)
            while max_seq_index in indexes:
                max_seq_index += 1

            # sending ACK
            cur_sock.sendto(bytes(f'{max_seq_index :< {ACK_SIZE}}', FORMAT), addr)
        # DONE
        if bytes_received >= msg_len:
            # sort chunks by index
            chunks = sorted(chunks, key=lambda chunk_: int(chunk_[LEN_SIZE_HEADER:LEN_INDEX_HEADER + LEN_SIZE_HEADER]))
            print("chunks 2", chunks)
            # combine chunks
            full_msg = b''
            for chunk in chunks:
                full_msg += chunk[LEN_SIZE_HEADER + LEN_INDEX_HEADER:]
            print("full:", full_msg)
            full_msg = pickle.loads(full_msg)  # todo: fix pickles- couldn't unpickle
            print("full 2:", full_msg)
            return full_msg
