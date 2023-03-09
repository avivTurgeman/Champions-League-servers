import pickle
import unittest
import socket
import time
import threading

import PL_player
import query_object
import DATA


class MyTestCase(unittest.TestCase):

    def test_tcp_server(self):
        pass

    def test_udp_server(self):
        pass

    def connection_with_dhcp(self, threading_=True):
        # connection
        DHCP_ADDR = (socket.gethostbyname(socket.gethostname()), 4836)
        dhcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dhcp_sock.connect(DHCP_ADDR)

        # request
        msg = pickle.dumps("PLEASE CONNECT ME")
        msg = bytes(f'{len(msg) :< {8}}', "utf-8") + msg
        dhcp_sock.send(msg)

        if threading_:
            time.sleep(0.5)

        # receive answer
        new_msg = True
        answer = b''
        msg_len = 0
        get_size = 8
        while True:
            msg = dhcp_sock.recv(get_size)
            if new_msg:
                msg_len = int(msg[:8])
                new_msg = False
                get_size = 32
            else:
                answer += msg
            if len(answer) == msg_len:
                answer = pickle.loads(answer)
                break

        # close connection
        msg = pickle.dumps("EXIT")
        msg = bytes(f'{len(msg) :< {8}}', "utf-8") + msg
        dhcp_sock.send(msg)
        dhcp_sock.close()

        if not threading_:
            return answer
        else:
            time.sleep(1)
            self.assertEqual(answer, [(socket.gethostbyname(socket.gethostname()), 20351),
                                      (socket.gethostbyname(socket.gethostname()), 5555)])

    def test_dhcp_server(self):
        # YOU HAVE TO RUN THE DHCP SERVER BEFORE RUNNING THIS TEST!!!
        answer = self.connection_with_dhcp(False)
        self.assertEqual([(socket.gethostbyname(socket.gethostname()), 20351),
                          (socket.gethostbyname(socket.gethostname()), 5555)], answer)

        client1 = threading.Thread(target=self.connection_with_dhcp)
        client2 = threading.Thread(target=self.connection_with_dhcp)
        client2.start()
        client1.start()

    def connection_with_dns(self, threading_=True):

        dns_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dns_sock.connect((socket.gethostbyname(socket.gethostname()), 5555))

        # request
        msg = pickle.dumps("SERVER")
        msg = bytes(f'{len(msg) :< {8}}', 'utf-8') + msg
        dns_sock.send(msg)

        if threading_:
            time.sleep(0.5)

        # receive answer
        new_msg = True
        answer = b''
        msg_len = 0
        get_size = 8
        while True:
            msg = dns_sock.recv(get_size)
            if new_msg:
                msg_len = int(msg[:8])
                new_msg = False
                get_size = 32
            else:
                answer += msg
            if len(answer) == msg_len:
                answer = pickle.loads(answer)
                break

        # close connection
        msg = pickle.dumps("EXIT")
        msg = bytes(f'{len(msg) :< {8}}', 'utf-8') + msg
        dns_sock.send(msg)
        dns_sock.close()

        if threading_:
            time.sleep(1)
            self.assertEqual((socket.gethostbyname(socket.gethostname()), 30015), answer)
        else:
            return answer

    def test_dns_server(self):
        # YOU HAVE TO RUN THE DNS SERVER BEFORE RUNNING THIS TEST!!!
        answer = self.connection_with_dns(False)
        self.assertEqual((socket.gethostbyname(socket.gethostname()), 30015), answer)

        client1 = threading.Thread(target=self.connection_with_dns)
        client2 = threading.Thread(target=self.connection_with_dns)
        client2.start()
        client1.start()

    def test_PL_player(self):
        alon = PL_player.PL_player("alon", 9.9, "Hapoel Revava", "CM", 3, 4)
        self.assertEqual("alon", alon.get_name())
        self.assertEqual(9.9, alon.get_rate())
        self.assertEqual("Hapoel Revava", alon.get_team())
        self.assertEqual("CM", alon.get_position())
        self.assertEqual(3, alon.get_goals())
        self.assertEqual(4, alon.get_assists())

    def test_query(self):
        top_scorer = query_object.query_obj("top scorer")
        exit_query = query_object.query_obj("exit", True)
        not_real_q = query_object.query_obj("lnsldlanfa")

        self.assertEqual([], not_real_q.do_query(DATA.data))
        self.assertEqual([DATA.data[11]], top_scorer.do_query(DATA.data))
        self.assertEqual(True, exit_query.is_exit())
        self.assertEqual(False, not_real_q.is_exit())


if __name__ == '__main__':
    unittest.main()
